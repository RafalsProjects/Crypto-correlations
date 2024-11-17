import yfinance as yf
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import matplotlib.pyplot as plt

# 1. Pobranie danych historycznych BTC z yfinance
def get_btc_data(start_date, end_date):
    btc = yf.download('BTC-USD', start=start_date, end=end_date)
    btc['Price'] = btc['Adj Close']
    return btc[['Price']]

# 2. Pobranie danych M2 z FRED API
def get_m2_data(start_date, end_date):
    m2_data = pdr.get_data_fred('M2', start=start_date, end=end_date)
    return m2_data

# 3. Funkcja do obliczania korelacji
def calculate_correlation(btc_data, m2_data):
    # Scalenie danych po dacie
    merged_data = pd.merge(btc_data, m2_data, left_index=True, right_index=True, how='inner')
    
    # Obliczanie korelacji
    correlation = merged_data['Price'].corr(merged_data['M2'])
    print(f"Korelacja między BTC a globalną podażą M2: {correlation}")
    
    return merged_data

# 4. Rysowanie wykresu
def plot_data(merged_data):
    plt.figure(figsize=(10,6))
    ax1 = merged_data['Price'].plot(label='BTC Price (USD)', color='blue')
    ax2 = merged_data['M2'].plot(secondary_y=True, label='M2 Money Supply', color='green')

    ax1.set_ylabel('BTC Price (USD)')
    ax2.set_ylabel('M2 Money Supply')

    plt.title('Bitcoin Price vs M2 Money Supply')
    plt.show()

# Ustawienia daty
start_date = datetime(2015, 1, 1)
end_date = datetime(2024, 1, 1)

# Pobranie danych
btc_data = get_btc_data(start_date, end_date)
m2_data = get_m2_data(start_date, end_date)

# Obliczanie korelacji i rysowanie wykresu
merged_data = calculate_correlation(btc_data, m2_data)
plot_data(merged_data)


print(m2_data.head())
print(m2_data.tail())
