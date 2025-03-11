import yfinance as yf
import matplotlib.pyplot as plt

# Set ticker to SPY
ticker = "SPY"

# Download historical data for SPY
data = yf.download(ticker, period="max", interval="1d")

# Plot the Close price versus the date (index)
plt.figure(figsize=(12, 6))
plt.plot(data.index, data["Close"], label="SPY Close Price")
plt.title("SPY Price History (Close)")
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
