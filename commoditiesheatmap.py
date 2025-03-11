import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.title("Commodity Price Dashboard (Debug Mode)")
st.write("""
**This version prints the DataFrame columns before plotting, so you can see exactly what's happening.**
""")

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

cols = 3
com_names = list(commodities.keys())
total = len(com_names)

for i in range(0, total, cols):
    row = st.columns(cols)
    
    for col, name in zip(row, com_names[i : i + cols]):
        ticker = commodities[name]
        
        # Download daily data for the maximum period
        df = yf.download(ticker, period="max", interval="1d")
        
        if df.empty:
            col.write(f"**No data returned for {name}**")
            continue
        
        # Flatten multi-level columns if necessary
        if isinstance(df.columns, pd.MultiIndex) and df.columns.nlevels > 1:
            df.columns = df.columns.droplevel(1)

        # Reset index so 'Date' becomes a column
        df.reset_index(inplace=True)  # If the index was the date, now it's a column named 'Date'

        # If you still see weird tuples, flatten them
        if isinstance(df.columns[0], tuple):
            df.columns = [c[0] for c in df.columns]
        
        # For debugging: let's print the first few rows and the columns
        with col.expander(f"Debug: {name} DataFrame Head & Columns"):
            col.write("Columns:", list(df.columns))
            col.write(df.head())

        # We want to ensure "Date" and "Close" exist
        if "Date" not in df.columns or "Close" not in df.columns:
            col.write(f"**Missing 'Date' or 'Close' columns for {name}**.")
            continue
        
        # Plot
        title = f"{name} Price History (Close)"
        try:
            fig = px.line(df, x="Date", y="Close", title=title)
            col.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            col.error(f"Could not plot {name}: {str(e)}")
