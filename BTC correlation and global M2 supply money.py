import requests
import pandas as pd

# URL do plików JSON
m2_url = "https://charts.bgeometrics.com/files/glm2.json"
btc_price_url = "https://charts.bgeometrics.com/files/glm2_btc_price.json"
m2_yoy_change_url = "https://charts.bgeometrics.com/files/m2_yoy_change.json"
m2_weeks7_change_url = "https://charts.bgeometrics.com/files/m2_weeks7_change.json"

def fetch_data(url):
    """Funkcja do pobierania danych z URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Błąd podczas pobierania danych z {url}: {response.status_code}")
        return None

# Pobieranie danych
m2_data = fetch_data(m2_url)
btc_price_data = fetch_data(btc_price_url)
m2_yoy_change_data = fetch_data(m2_yoy_change_url)
m2_weeks7_change_data = fetch_data(m2_weeks7_change_url)

# Konwersja do DataFrame
if m2_data is not None:
    m2_df = pd.DataFrame(m2_data)
    
if btc_price_data is not None:
    btc_price_df = pd.DataFrame(btc_price_data)

# Obliczanie korelacji
if m2_df is not None and btc_price_df is not None:
    # Ustawianie nazw kolumn dla DataFrame
    m2_df.columns = ['Timestamp', 'M2']
    btc_price_df.columns = ['Timestamp', 'BTC_Price']

    # Łączenie DataFrame na podstawie znacznika czasu
    merged_df = pd.merge(m2_df, btc_price_df, on='Timestamp')

    # Obliczanie korelacji
    correlation = merged_df['M2'].corr(merged_df['BTC_Price'])
    print(f"Korelacja między M2 a ceną BTC: {correlation}")

# Łączenie wszystkich DataFrame w jeden
all_data = pd.concat([m2_df, btc_price_df, pd.DataFrame(m2_yoy_change_data, columns=['Timestamp', 'M2_YoY_Change']),
                       pd.DataFrame(m2_weeks7_change_data, columns=['Timestamp', 'M2_Weeks7_Change'])], axis=1)

# Wyświetlanie wynikowego DataFrame
print(all_data)


# URL to check what data is here
# https://charts.bgeometrics.com/m2_global.html
# The money supply data has been taken from 21 central banks.
# From North America Data: USM and CAM
# From the Eurozone: EUM
# From non-eurozone Europe: CHM, GBM, FIPOP and RUM
# From Pacific: NZM
# From Asia: CNM, TWM, HKM, INM, JPM, PHM and SGM
# From Latin America: BRM, COM and MXM
# From Middle East: AEM and TRM
# From Africa: ZAM.