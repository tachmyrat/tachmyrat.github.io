import pandas as pd
import matplotlib.pyplot as plt

# Open CSV file
data = pd.read_csv('/home/kkk/Downloads/archive/Solana Historical Data.csv')

# Display the data
print(data.head())

# Convert 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'], format='%b %d, %Y')

# Clean the Price column and convert to float
data['Price'] = data['Price'].astype(float)

# Now you can plot
plt.figure(figsize=(10, 5))
plt.plot(data['Date'], data['Price'], marker='o')
plt.title('Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid()

# Save the plot to a file
plt.savefig('price_over_time.png')
