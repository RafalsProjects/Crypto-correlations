import requests
import pandas as pd

# Parametry
api_key = '3e2186af9e0db2c0ab8ff1209ed9d2baa0fcf8c298f4e55f55751f3a9e52'
coin_symbol = 'BTC'  # Symbol Bitcoina
convert = 'USD'
time_start = '2024-09-09'
time_end = '2024-10-09'
interval = 'daily'

# Funkcja do pobierania danych historycznych
def fetch_historical_data(coin_symbol, convert, time_start, time_end, interval):
    url = 'https://api.cryptorank.io/v1/currencies/historical'
    params = {
        'convert': convert,
        'time_start': time_start,
        'time_end': time_end,
        'interval': interval,
        'symbols': coin_symbol,
        'api_key': api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data['data'])
    else:
        print(f"Error fetching historical market cap data for {coin_symbol}: {response.status_code} Client Error: {response.text}")
        return pd.DataFrame()

# Pobierz dane historyczne
bitcoin_data = fetch_historical_data(coin_symbol, convert, time_start, time_end, interval)

# Sprawdź dane
print(bitcoin_data)
