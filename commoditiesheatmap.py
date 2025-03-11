import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# --------------------------------------------------------------------------------
# Set up Streamlit page
# --------------------------------------------------------------------------------
st.set_page_config(layout="wide")
st.title("Commodities & Cryptos Dashboard (Sorted by Z‑Score)")

# --------------------------------------------------------------------------------
# Default Dictionaries
# --------------------------------------------------------------------------------
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

cryptos = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Ripple": "XRP-USD",
    "Litecoin": "LTC-USD",
    "Bitcoin Cash": "BCH-USD",
    "Cardano": "ADA-USD",
    "Polkadot": "DOT-USD"
}

# --------------------------------------------------------------------------------
# Callback functions for "Clear" and "Insert" buttons
# --------------------------------------------------------------------------------
def clear_dashboard():
    st.session_state["commodity_select"] = []
    st.session_state["custom_input"] = ""

def insert_commodities():
    st.session_state["commodity_select"] = list(commodities.keys())

# --------------------------------------------------------------------------------
# Sidebar Controls
# --------------------------------------------------------------------------------
st.sidebar.header("Dashboard Controls")

# Number of columns per row (1-10)
cols_per_row = st.sidebar.slider("Number of columns per row", min_value=1, max_value=10, value=3, step=1)

# Timeframe controls
st.sidebar.header("Select Timeframe")
period = st.sidebar.selectbox(
    "Period",
    ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
    index=10  # default "max"
)
interval = st.sidebar.selectbox(
    "Interval",
    ["1m", "2m", "5m", "15m", "30m", "60m", "1h", "1d", "5d", "1wk", "1mo", "3mo"],
    index=7   # default "1d"
)

st.sidebar.write("""
**Note**: Some period/interval combinations are not supported by Yahoo Finance.
If a chart is empty, try a shorter period or a longer interval.
""")

# Let user exclude after-hours for intraday intervals
exclude_afterhours = st.sidebar.checkbox("Exclude After‑Hours", value=True)

# Commodity selection
selected = st.sidebar.multiselect(
    "Select commodities to display:",
    options=list(commodities.keys()),
    default=list(commodities.keys()),
    key="commodity_select"
)

# Custom ticker input
custom_input = st.sidebar.text_input(
    "Enter additional ticker symbols (comma-separated):",
    value="",
    key="custom_input"
)

# Buttons for clearing or inserting commodities
st.sidebar.button("Clear Dashboard", on_click=clear_dashboard)
st.sidebar.button("Insert Commodities", on_click=insert_commodities)

# Checkbox: Include Cryptos
include_crypto = st.sidebar.checkbox("Include Cryptos")

# --------------------------------------------------------------------------------
# Build the Dashboard Dictionary
# --------------------------------------------------------------------------------
dashboard = {}

# Add selected commodities
for name in st.session_state.get("commodity_select", selected):
    dashboard[name] = commodities[name]

# Add custom tickers
custom_tickers = [t.strip() for t in st.session_state.get("custom_input", custom_input).split(",") if t.strip()]
for ticker in custom_tickers:
    dashboard[ticker] = ticker

# Optionally add cryptos
if include_crypto:
    for name, ticker in cryptos.items():
        dashboard[name] = ticker

# --------------------------------------------------------------------------------
# Data Fetching (with intraday filtering) and Z‑Score Computation
# --------------------------------------------------------------------------------
@st.cache_data
def get_clean_data(ticker: str, period: str, interval: str, exclude_afterhours: bool):
    """
    Download data from Yahoo Finance, flatten columns if needed,
    and (optionally) remove weekends and after-hours for intraday intervals.
    """
    # Download data; prepost=False excludes pre/post market
    data = yf.download(ticker, period=period, interval=interval, prepost=False)

    # Flatten columns if MultiIndex
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # If this is an intraday interval and the user wants to exclude after-hours
    # then remove weekends and keep only 9:30–16:00 for US markets.
    if exclude_afterhours and (interval.endswith("m") or interval.endswith("h")):
        if not data.empty and isinstance(data.index, pd.DatetimeIndex):
            # Remove weekends
            data = data[data.index.dayofweek < 5]
            # Keep only 9:30–16:00
            data = data.between_time("09:30", "16:00")

    return data

def compute_zscore(prices: pd.Series) -> float:
    """Compute the z-score of the most recent price relative to the price history."""
    if prices.empty:
        return np.nan
    mean_price = prices.mean()
    std_price = float(prices.std())
    if std_price == 0:
        return np.nan
    last_price = prices.iloc[-1]
    return (last_price - mean_price) / std_price

# Collect data and compute z‑scores
items_data = []
for name, ticker in dashboard.items():
    data = get_clean_data(ticker, period, interval, exclude_afterhours)
    if data.empty:
        zscore = np.nan
    else:
        zscore = compute_zscore(data["Close"])
    items_data.append({
        "name": name,
        "ticker": ticker,
        "data": data,
        "zscore": zscore
    })

# Sort by z‑score ascending (NaN last)
items_data = sorted(items_data, key=lambda x: (np.isnan(x["zscore"]), x["zscore"]))

# --------------------------------------------------------------------------------
# Display Charts in a Grid
# --------------------------------------------------------------------------------
for i in range(0, len(items_data), cols_per_row):
    cols = st.columns(cols_per_row)
    for j, item in enumerate(items_data[i : i + cols_per_row]):
        with cols[j]:
            name = item["name"]
            ticker = item["ticker"]
            data = item["data"]
            zscore = item["zscore"]

            if data.empty:
                st.write(f"No data available for {name} ({ticker})")
            else:
                fig, ax = plt.subplots(figsize=(4, 3))
                ax.plot(data.index, data["Close"], linewidth=1)
                ax.set_title(f"{name} ({ticker})\nz = {zscore:.2f}", fontsize=9)
                ax.tick_params(axis="x", labelrotation=45, labelsize=6)
                ax.tick_params(axis="y", labelsize=6)
                ax.set_xlabel("")
                ax.set_ylabel("")
                plt.tight_layout()
                st.pyplot(fig)
