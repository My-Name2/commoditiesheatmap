import yfinance as yf
import plotly.express as px
import pandas as pd

# Choose a commodity (Gold in this example)
ticker = "GC=F"
data = yf.download(ticker, period="max", interval="1d").reset_index()

# Flatten the columns if they are tuples (or a MultiIndex)
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)
elif isinstance(data.columns[0], tuple):
    data.columns = [col[0] for col in data.columns]

# Now "Date" is a valid column name.
fig = px.line(data, x="Date", y="Close", title="Gold Price History (Close)")
fig.show()
