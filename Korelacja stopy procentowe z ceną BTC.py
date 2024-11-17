import pandas as pd
import requests
from pandas_datareader import data as pdr
import datetime

# Ustawienia dat
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=365)

# 1. Pobieranie danych BTC z CoinGecko
def fetch_btc_data(interval='daily'):
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': '365',
        'interval': interval
    }
    response = requests.get(url, params=params)
    btc_data = response.json()
    
    # Konwertowanie na DataFrame
    btc_prices = pd.DataFrame(btc_data['prices'], columns=['timestamp', 'price'])
    btc_prices['timestamp'] = pd.to_datetime(btc_prices['timestamp'], unit='ms')
    btc_prices.set_index('timestamp', inplace=True)
    
    # Zmiana nazw kolumn
    btc_prices.rename(columns={'price': 'btc_price'}, inplace=True)
    return btc_prices

# 2. Pobieranie danych o stopach procentowych z FRED
def fetch_interest_rates(interval='D'):
    rates = ['FEDFUNDS', 'GS5', 'GS10', 'GS30']
    interest_rate_data = {}

    for rate in rates:
        data = pdr.get_data_fred(rate, start_date, end_date)
        interest_rate_data[rate] = data.rename(columns={rate: f'{rate}_rate'})

    # Łączenie wszystkich stóp w jeden DataFrame
    combined_interest_rates = pd.concat(interest_rate_data.values(), axis=1)

    # Zmiana interwału danych
    if interval == 'W':
        combined_interest_rates = combined_interest_rates.resample('W').mean()
    else:
        combined_interest_rates = combined_interest_rates.resample('D').mean()
    
    # Wypełnianie brakujących wartości
    combined_interest_rates.ffill(inplace=True)

    return combined_interest_rates

# 3. Obliczanie korelacji
def calculate_correlation(btc_prices, interest_rates):
    # Łączenie DataFrame
    combined_data = btc_prices.join(interest_rates)
    
    # Usuwanie wierszy z NaN
    combined_data.dropna(inplace=True)
    
    # Obliczanie korelacji dla wszystkich stóp
    correlation = combined_data.corr().loc['btc_price']

    # Tworzenie pustych kolumn dla korelacji
    for rate in ['FEDFUNDS_rate', 'GS5_rate', 'GS10_rate', 'GS30_rate']:
        combined_data[f'Korelacja_{rate}'] = None

    # Wstawianie wartości korelacji w jednym wierszu (pierwszym)
    for rate in ['FEDFUNDS_rate', 'GS5_rate', 'GS10_rate', 'GS30_rate']:
        combined_data.at[combined_data.index[0], f'Korelacja_{rate}'] = correlation[rate]
    
    return combined_data

# Zapis do pliku CSV
def save_to_csv(dataframe, filename):
    dataframe.to_csv(filename)

# Główna logika
btc_prices = fetch_btc_data(interval='daily')  # Można zmienić na 'weekly'
interest_rates = fetch_interest_rates(interval='D')  # Można zmienić na 'W'
combined_data = calculate_correlation(btc_prices, interest_rates)

print("Dane z korelacjami:\n", combined_data)

# Zapis danych do pliku CSV
save_to_csv(combined_data, 'btc_interest_rates_data.csv')
print("Dane zostały zapisane do pliku 'btc_interest_rates_data.csv'.")
