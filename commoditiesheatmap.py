import yfinance as yf
import pandas as pd
import plotly.express as px

# Choose a commodity ticker (Gold in this example)
ticker = "GC=F"
data = yf.download(ticker, period="max", interval="1d").reset_index()

# Flatten the DataFrame columns if they are a MultiIndex
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.map(lambda x: x[0])

# Now plot the chart using Plotly Express
fig = px.line(data, x="Date", y="Close", title="Gold Price History (Close)")
fig.show()
