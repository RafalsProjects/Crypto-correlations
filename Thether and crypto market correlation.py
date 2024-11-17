import requests
import pandas as pd
import time

# Funkcja do pobierania historycznej kapitalizacji rynkowej danego tokena z CoinGecko
def get_market_cap_data(coin_id, vs_currency="usd", days="365"):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": days
    }
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return None
    
    data = response.json()
    if 'market_caps' not in data:
        print("Brak danych 'market_caps' w odpowiedzi.")
        return None
    
    market_caps = data['market_caps']
    
    # Konwersja do DataFrame z kolumnami 'date' i 'market_cap'
    df = pd.DataFrame(market_caps, columns=['timestamp', 'market_cap'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.drop('timestamp', axis=1, inplace=True)
    
    return df

# Pobranie danych kapitalizacji Tethera (USDT)
tether_data = get_market_cap_data('tether')
time.sleep(2)

# Pobranie danych kapitalizacji Bitcoina (BTC)
bitcoin_data = get_market_cap_data('bitcoin')
time.sleep(2)

# Pobranie danych kapitalizacji USDC (zmień na 'usd-coin')
usdc_data = get_market_cap_data('usd-coin')  # Użyj poprawnego identyfikatora
time.sleep(2)

if tether_data is not None and bitcoin_data is not None and usdc_data is not None:
    # Połączenie danych na podstawie dat w dwóch krokach
    merged_data_1 = pd.merge(tether_data, bitcoin_data, on='date', suffixes=('_tether', '_bitcoin'))
    
    # Łączymy z danymi USDC, dodając sufiks
    merged_data = pd.merge(merged_data_1, usdc_data.rename(columns={'market_cap': 'market_cap_usd_coin'}), on='date', suffixes=('', '_usd_coin'))
    
    # Wyświetlenie struktury merged_data
    print("Merged DataFrame:")
    print(merged_data.head())  # Pokaż pierwsze wiersze

    # Sprawdź, czy kolumny są dostępne
    print("Kolumny w merged_data:", merged_data.columns.tolist())
    
    # Obliczenie korelacji
    correlation_usdt_btc = merged_data['market_cap_tether'].corr(merged_data['market_cap_bitcoin'])
    correlation_usdc_btc = merged_data['market_cap_usd_coin'].corr(merged_data['market_cap_bitcoin'])

    print(f"Korelacja między kapitalizacją rynkową Tethera a kapitalizacją Bitcoina: {correlation_usdt_btc:.2f}")
    print(f"Korelacja między kapitalizacją rynkową USDC a kapitalizacją Bitcoina: {correlation_usdc_btc:.2f}")

    
    # Dodanie kolumny 'Korelacja BTC/USDT' oraz 'Korelacja BTC/USDC'
    merged_data['Korelacja BTC/USDT'] = None
    merged_data['Korelacja BTC/USDC'] = None

    # Przypisanie korelacji do DataFrame
    merged_data.iloc[0, 4] = correlation_usdt_btc  # Przypisz korelację USDT-BTC
    merged_data.iloc[0, 5] = correlation_usdc_btc  # Przypisz korelację USDC-BTC

    # Przemieszanie kolumn tak, aby data była pierwsza, a korelacja ostatnia
    merged_data = merged_data[['date', 'market_cap_tether', 'market_cap_bitcoin', 'market_cap_usd_coin', 'Korelacja BTC/USDT', 'Korelacja BTC/USDC']]
    
    # Zapis danych do pliku Excel
    file_path = "USD_major_coins_and_bitcoin_correlation.xlsx"
    merged_data.to_excel(file_path, index=False)
    
    print(f"Dane zapisane do pliku: {file_path}")
else:
    print("Nie udało się pobrać danych.")

