import requests

def fetch_coin_list(api_key):
    url = "https://api.cryptorank.io/v1/currencies"
    params = {
        'api_key': '3e2186af9e0db2c0ab8ff1209ed9d2baa0fcf8c298f4e55f55751f3a9e52',
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data['data']  # Zwracamy listę dostępnych kryptowalut
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coin list: {e}")
        return []

if __name__ == "__main__":
    api_key = '3e2186af9e0db2c0ab8ff1209ed9d2baa0fcf8c298f4e55f55751f3a9e52'  # Wstaw swój klucz API tutaj
    coins = fetch_coin_list(api_key)
    
    
    for coin in coins:
        print(f"ID: {coin['id']}, Name: {coin['name']}, Symbol: {coin['symbol']}")
