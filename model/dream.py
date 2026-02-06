import requests
import pandas as pd

# Function to get current BTC price
def get_current_btc_price():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'bitcoin',
        'vs_currencies': 'usd'  # You can change this to other currencies as needed
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['bitcoin']['usd']

# Function to get historical BTC prices
def get_historical_btc_prices(start_date, end_date):
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range'
    params = {
        'vs_currency': 'usd',
        'from': start_date,  # Unix timestamp
        'to': end_date       # Unix timestamp
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['prices']  # Returns a list of [timestamp, price]

# Get current BTC price
current_price = get_current_btc_price()
print(f'Current Bitcoin Price: ${current_price}')

# Get historical BTC prices (example: last 30 days)
import time
end_time = int(time.time())  # Current time in seconds since epoch
start_time = end_time - (30 * 24 * 60 * 60)  # 30 days ago

historical_prices = get_historical_btc_prices(start_time, end_time)

# Convert historical prices to DataFrame for better visualization
historical_df = pd.DataFrame(historical_prices, columns=['timestamp', 'price'])
historical_df['date'] = pd.to_datetime(historical_df['timestamp'], unit='ms')  # Convert timestamp to datetime
historical_df.drop('timestamp', axis=1, inplace=True)  # Remove the timestamp column if not needed

print(historical_df)
