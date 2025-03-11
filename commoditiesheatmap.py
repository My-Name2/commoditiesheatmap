import yfinance as yf
import plotly.express as px
import streamlit as st
import pandas as pd

st.title("Commodity Price Dashboard")
st.markdown("This dashboard displays historical closing prices for various commodities.")

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

# Set the number of columns for the dashboard grid
cols = 3
commodity_names = list(commodities.keys())
n = len(commodity_names)

# Loop over commodities in groups of 'cols' and display each chart in its own Streamlit column
for i in range(0, n, cols):
    columns = st.columns(cols)
    for col, name in zip(columns, commodity_names[i:i+cols]):
        ticker = commodities[name]
        data = yf.download(ticker, period="max", interval="1d").reset_index()
        
        # Flatten multi-index columns if present
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col_item[0] for col_item in data.columns]
        
        # Ensure "Date" column exists
        if "Date" not in data.columns:
            data = data.rename(columns={data.columns[0]: "Date"})
        
        # Create the Plotly Express line chart
        fig = px.line(data, x="Date", y="Close", title=f"{name} Price History (Close)")
        
        col.plotly_chart(fig, use_container_width=True)
