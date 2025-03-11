import yfinance as yf
import plotly.express as px
import streamlit as st
import pandas as pd

st.title("Commodity Price Dashboard")
st.markdown("This dashboard displays historical closing prices for various commodities using Plotly Express.")

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

# Set the number of columns for the grid layout
cols = 3
commodity_names = list(commodities.keys())
n = len(commodity_names)

# Iterate over commodities in groups of 'cols'
for i in range(0, n, cols):
    columns = st.columns(cols)
    for col, name in zip(columns, commodity_names[i:i+cols]):
        ticker = commodities[name]
        data = yf.download(ticker, period="max", interval="1d").reset_index()
        
        # If data is empty, display a message and skip plotting
        if data.empty:
            col.write(f"No data available for {name}.")
            continue
        
        # If the columns are a MultiIndex, flatten them
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        # Also check if the first column is a tuple (i.e., columns like ("Date", ""))
        elif isinstance(data.columns[0], tuple):
            data.columns = [col_item[0] for col_item in data.columns]
        
        # Ensure the "Date" column exists; if not, rename the first column to "Date"
        if "Date" not in data.columns:
            data = data.rename(columns={data.columns[0]: "Date"})
        
        # Create a Plotly Express line chart
        try:
            fig = px.line(data, x="Date", y="Close", title=f"{name} Price History (Close)")
        except Exception as e:
            col.write(f"Error plotting {name}: {e}")
            continue
        
        # Display the Plotly chart in the corresponding Streamlit column
        col.plotly_chart(fig, use_container_width=True)
