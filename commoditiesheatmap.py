import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.title("Commodity Price Viewer")

# Define commodities and their ticker symbols
commodities = {
    "Gold": "GC=F",
    "Silver": "SI=F",
    "Crude Oil": "CL=F",
    "Brent Crude Oil": "BZ=F",
    "Natural Gas": "NG=F",
    "Corn": "ZC=F",
    "Wheat": "ZW=F",
    "Soybeans": "ZS=F",
    "Copper": "HG=F",
    "Palladium": "PA=F",
    "Platinum": "PL=F",
    "Cotton": "CT=F",
    "Coffee": "KC=F",
    "Sugar": "SB=F",
    "Cocoa": "CC=F",
    "Live Cattle": "LE=F",
    "Lean Hogs": "HE=F",
    "Feeder Cattle": "GF=F",
    "Oats": "ZO=F",
    "Orange Juice": "OJ=F"
}

# Let the user select a commodity
selected_commodity = st.selectbox("Select a Commodity", list(commodities.keys()))
ticker = commodities[selected_commodity]

st.write(f"Fetching data for {selected_commodity}...")
data = yf.download(ticker, period="max", interval="1d").reset_index()

# Flatten the DataFrame columns if they are a MultiIndex
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# Check if data is available
if data.empty:
    st.write("No data available for", selected_commodity)
else:
    # Create a Plotly line chart of the closing price
    fig = px.line(data, x="Date", y="Close", title=f"{selected_commodity} Price History (Close)")
    st.plotly_chart(fig, use_container_width=True)
