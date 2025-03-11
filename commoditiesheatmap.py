import yfinance as yf
import matplotlib.pyplot as plt

# Choose a commodity
commodity = "Gold"
ticker = "GC=F"

# Download historical data
data = yf.download(ticker, period="max", interval="1d")

# Create a matplotlib figure and plot the Close prices
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["Close"], label="Close Price")
plt.title(f"{commodity} Price History (Close)")
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# Save the plot as an image file
image_file = "commodity_chart.png"
plt.savefig(image_file)
plt.show()

print(f"Chart saved to {image_file}")
