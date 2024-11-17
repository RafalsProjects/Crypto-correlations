import pandas as pd
import requests
from pandas_datareader import data as pdr
import datetime

# Ustawienia dat
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=365)

# 1. Pobieranie dostępnych kryptowalut z CoinGecko
def fetch_all_coins():
    url = 'https://api.coingecko.com/api/v3/coins/list'
    response = requests.get(url)
    
    # Konwertowanie odpowiedzi na DataFrame
    coins = pd.DataFrame(response.json())
    
    # Wyświetlanie listy kryptowalut (nazwa i symbol)
    print("Lista dostępnych kryptowalut:")
    print(coins[['id', 'symbol', 'name']])
    coins.to_csv('available_coins.csv', index=False)
    print("Lista kryptowalut została zapisana do pliku 'available_coins.csv'.")
    return coins

# 2. Pobieranie danych dla wybranego coina z CoinGecko
def fetch_coin_data(coin_symbol, interval='daily'):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_symbol}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': '365',
        'interval': interval
    }
    response = requests.get(url, params=params)
    coin_data = response.json()
    
    # Konwertowanie na DataFrame
    coin_prices = pd.DataFrame(coin_data['prices'], columns=['timestamp', 'price'])
    coin_prices['timestamp'] = pd.to_datetime(coin_prices['timestamp'], unit='ms')
    coin_prices.set_index('timestamp', inplace=True)
    
    # Zmiana nazw kolumn
    coin_prices.rename(columns={'price': f'{coin_symbol}_price'}, inplace=True)
    return coin_prices

# 3. Pobieranie danych o stopach procentowych z FRED
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

# 4. Obliczanie korelacji
def calculate_correlation(coin_prices, interest_rates, coin_symbol):
    # Łączenie DataFrame
    combined_data = coin_prices.join(interest_rates)
    
    # Usuwanie wierszy z NaN
    combined_data.dropna(inplace=True)
    
    # Obliczanie korelacji dla wszystkich stóp
    correlation = combined_data.corr().loc[f'{coin_symbol}_price']

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
coins_list = fetch_all_coins()  # Pobieranie i wyświetlanie listy kryptowalut

# Zmienna z symbolem coina
coin_symbol = 'maker'  # Możesz tutaj ustawić wybrany symbol kryptowaluty

# Pobieranie danych dla wybranego coina
coin_prices = fetch_coin_data(coin_symbol, interval='daily')  # Można zmienić na 'weekly'
interest_rates = fetch_interest_rates(interval='D')  # Można zmienić na 'W'

# Obliczanie korelacji
combined_data = calculate_correlation(coin_prices, interest_rates, coin_symbol)

# Wyświetlanie danych
print(f"Dane z korelacjami dla {coin_symbol}:\n", combined_data)

# Zapis danych do pliku CSV
save_to_csv(combined_data, f'{coin_symbol}_interest_rates_data.csv')
print(f"Dane zostały zapisane do pliku '{coin_symbol}_interest_rates_data.csv'.")
