import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.title("Gold Price History (1 Year)")

# Download one year of daily Gold data
data = yf.download("GC=F", period="1y", interval="1d")
data = data.reset_index()

# Flatten multi-index columns, if present
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# Create a line chart of the closing price
fig = px.line(data, x="Date", y="Close", title="Gold Price History (1 Year)")
st.plotly_chart(fig)
