import pandas as pd
import numpy as np
import requests
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Function to get historical BTC prices
import requests
import pandas as pd
import time

#from binance.client import Client
from binance.client import Client

# Initialize the client
api_key = 'sDkRWAS6jmX0FX5a8VQrgNXfOHCPES5QGDU3HaE8xX7sLLT954ioUPAruGbrRbA6'
api_secret = 'YIcgzJMqo1GvKLOFObaQGzoV4REjhWVWTA1SXMWylNmKyr51Qa3fYjjAMESOc02S'
client = Client(api_key, api_secret)

# Fetch historical BTC/USDT data (e.g., daily candles)
def get_historical_btc_prices(symbol='BTCUSDT', interval='1d', start_date='30 days ago UTC'):
    candles = client.get_historical_klines(symbol, interval, start_date)
    data = pd.DataFrame(candles, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
        'quote_asset_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'
    ])
    data['date'] = pd.to_datetime(data['timestamp'], unit='ms')
    data['close'] = data['close'].astype(float)  # Convert closing prices to float
    return data[['date', 'close']]  # Return just date and close price columns

# Fetch the last 30 days of BTC prices
btc_data = get_historical_btc_prices()
print(btc_data)


# Fetch BTC prices from Binance
start_date = "2023-01-01"
end_date = "2023-12-01"
btc_prices = get_binance_btc_prices(start_date, end_date)
print(btc_prices)
data = pd.read_csv('/home/kkk/Downloads/archive/Solana Historical Data.csv')

# Clean and prepare the Solana data
data['Date'] = pd.to_datetime(data['Date'], format='%b %d, %Y')  # Adjusted format for abbreviated month
data['Price'] = data['Price'].astype(float)  # Convert price to float
data.sort_values('Date', inplace=True)

# Get historical BTC prices for the same date range as the Solana data
start_time = int(data['Date'].min().timestamp())
end_time = int(data['Date'].max().timestamp())
historical_prices = get_historical_btc_prices(start_time, end_time)

if historical_prices is None:
    print("Failed to fetch historical BTC prices. Exiting.")
    exit()

# Convert historical BTC prices to DataFrame
btc_df = pd.DataFrame(historical_prices, columns=['timestamp', 'BTC_Price'])
btc_df['Date'] = pd.to_datetime(btc_df['timestamp'], unit='ms')  # Convert timestamp to datetime
btc_df.drop('timestamp', axis=1, inplace=True)  # Remove the timestamp column if not needed

# Merge Solana and Bitcoin DataFrames on the 'Date' column
merged_data = pd.merge(data, btc_df, on='Date', how='inner')

# Create features: lag feature for Solana price
merged_data['Prev_Price'] = merged_data['Price'].shift(1)
merged_data.dropna(inplace=True)  # Drop NaN values after shifting

# Select features and target
X = merged_data[['Prev_Price', 'BTC_Price']]  # Include BTC price as a feature
y = merged_data['Price']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Prepare results for plotting
results = pd.DataFrame({
    'Date': merged_data['Date'].iloc[-len(y_test):].values,  # Test set dates
    'Actual Price': y_test.values,
    'Predicted Price': y_pred
})

print(results)  # Display actual and predicted prices

# Plot actual vs predicted prices
plt.figure(figsize=(10, 5))
plt.plot(results['Date'], results['Actual Price'], label='Actual Prices', marker='o')
plt.plot(results['Date'], results['Predicted Price'], label='Predicted Prices', marker='o')
plt.title('Actual vs Predicted Prices')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid()
plt.show()
