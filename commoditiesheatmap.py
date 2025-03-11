import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd

# Streamlit app title
st.title("Commodity Price Dashboard")
st.markdown("""
Displays long-term historical closing prices (daily) for each commodity using Plotly.
""")

# Define the commodities and their ticker symbols
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

# How many columns in each row
cols = 3
commodity_names = list(commodities.keys())
total = len(commodity_names)

# Loop over commodities in chunks of 'cols'
for i in range(0, total, cols):
    columns = st.columns(cols)
    # For each commodity in this row
    for col, name in zip(columns, commodity_names[i : i + cols]):
        ticker = commodities[name]
        
        # Download historical data (max period, daily interval)
        df = yf.download(ticker, period="max", interval="1d")
        
        # If no data is returned, skip
        if df.empty:
            col.write(f"No data available for {name}.")
            continue
        
        # Drop the second level of columns if it exists (commonly the ticker name):
        # Resulting columns should be: Open, High, Low, Close, Adj Close, Volume
        if isinstance(df.columns, pd.MultiIndex):
            # Safely check if there is indeed a second level
            if df.columns.nlevels > 1:
                df.columns = df.columns.droplevel(1)
        
        # Reset index so "Date" is a column
        df.reset_index(inplace=True)
        
        # Make sure we have "Date" and "Close" columns
        # (After droplevel, the DataFrame should have columns: 
        #  ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"])
        if "Date" not in df.columns or "Close" not in df.columns:
            col.write(f"Required columns not found for {name}. Columns are: {list(df.columns)}")
            continue

        # Plot with Plotly Express
        title = f"{name} Price History (Close)"
        try:
            fig = px.line(df, x="Date", y="Close", title=title)
            col.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            col.error(f"Could not plot {name}: {str(e)}")
