import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Use wide layout so the dashboard spans the entire page
st.set_page_config(layout="wide")

st.title("Commodities Dashboard")

# Define the default commodities and their ticker symbols.
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

# Let users choose which default commodities to display.
selected = st.multiselect(
    "Select commodities to display",
    options=list(commodities.keys()),
    default=list(commodities.keys())
)

# Allow users to add additional tickers via comma-separated input.
custom_input = st.text_input("Enter additional ticker symbols (comma-separated)", value="")
custom_tickers = [t.strip() for t in custom_input.split(",") if t.strip()]

# Build the dashboard dictionary: display name -> ticker symbol.
dashboard = {}
for name in selected:
    dashboard[name] = commodities[name]
for ticker in custom_tickers:
    dashboard[ticker] = ticker  # For custom tickers, the name is the same as the ticker.

# Removed the line that displayed the keys
# st.write("Displaying charts for:", list(dashboard.keys()))

# Cache the data download to speed up app performance.
@st.cache_data
def get_data(ticker):
    return yf.download(ticker, period="max", interval="1d")

# Set number of charts per row
cols_per_row = 3
dashboard_items = list(dashboard.items())

# Create a grid of charts.
for i in range(0, len(dashboard_items), cols_per_row):
    cols = st.columns(cols_per_row)
    for j, (name, ticker) in enumerate(dashboard_items[i : i + cols_per_row]):
        with cols[j]:
            # Removed subheader so no commodity name appears
            data = get_data(ticker)
            if data.empty:
                st.write("No data available for", ticker)
            else:
                fig, ax = plt.subplots(figsize=(4, 3))
                ax.plot(data.index, data["Close"])
                ax.tick_params(axis="x", labelrotation=45, labelsize=6)
                ax.tick_params(axis="y", labelsize=6)
                ax.set_xlabel("")
                ax.set_ylabel("")
                plt.tight_layout()
                st.pyplot(fig)
