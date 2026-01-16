import yfinance as yf

ticker = 'TSLA'
filename = 'TSLA_prices.csv'

# Download the maximum available data
data = yf.download(ticker, period="max")

# Save the data to the specific filename
data.to_csv(filename)

print(f"File '{filename}' has been created successfully.")
