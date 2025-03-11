import yfinance as yf
import plotly.express as px
import pandas as pd

# Set ticker to SPY
ticker = "SPY"

# Download historical data for SPY and reset the index to get the Date column
data = yf.download(ticker, period="max", interval="1d").reset_index()

# Flatten columns if they are a MultiIndex (not needed for SPY, but safe to include)
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# Create an interactive line chart with Plotly Express
fig = px.line(data, x="Date", y="Close", title="SPY Price History (Close)")
fig.show()
