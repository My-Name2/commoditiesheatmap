import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")  # Use the full width of the browser

st.title("Commodities Dashboard (Sorted by Z‑Score)")

# Define default commodities and their ticker symbols
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

# Let users pick which default commodities to display
selected = st.multiselect(
    "Select commodities to display:",
    options=list(commodities.keys()),
    default=list(commodities.keys())
)

# Let users add additional tickers (comma-separated)
custom_input = st.text_input("Enter additional ticker symbols (comma-separated):", "")
custom_tickers = [t.strip() for t in custom_input.split(",") if t.strip()]

# Build the final list of items to display: {display_name: ticker}
dashboard = {}
for name in selected:
    dashboard[name] = commodities[name]
for ticker in custom_tickers:
    # For custom tickers, use the same string for both name and ticker
    dashboard[ticker] = ticker

# Timeframe controls in the sidebar
st.sidebar.header("Select Timeframe")
period = st.sidebar.selectbox(
    "Period",
    ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
    index=10  # default to "max"
)
interval = st.sidebar.selectbox(
    "Interval",
    ["1m", "2m", "5m", "15m", "30m", "60m", "1h", "1d", "5d", "1wk", "1mo", "3mo"],
    index=7   # default to "1d"
)

st.sidebar.write("""
**Note**: Some period/interval combinations are not supported by Yahoo Finance.
If a chart is empty, try a shorter period or a longer interval.
""")

# Allow user to adjust the number of columns per row (from 1 to 10)
cols_per_row = st.sidebar.slider("Number of columns per row", min_value=1, max_value=10, value=3, step=1)

# Cache data to speed up repeated downloads
@st.cache_data
def get_data(ticker, period, interval):
    return yf.download(ticker, period=period, interval=interval)

def compute_zscore(prices: pd.Series) -> float:
    """
    Compute the z-score of the most recent price relative to the entire price history.
    z = (last_price - mean) / std
    Returns np.nan if std is 0 or if prices is empty.
    """
    if prices.empty:
        return np.nan
    mean_price = prices.mean()
    std_price = prices.std()
    if std_price == 0:
        return np.nan
    last_price = prices.iloc[-1]
    return (last_price - mean_price) / std_price

# 1. Collect data and compute z‑scores for each commodity
items_data = []
for name, ticker in dashboard.items():
    data = get_data(ticker, period, interval)
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

# 2. Sort by z‑score ascending (lowest first = "cheapest")
items_data = sorted(items_data, key=lambda x: (np.isnan(x["zscore"]), x["zscore"]))

# 3. Display the charts in a grid
items = items_data
for i in range(0, len(items), cols_per_row):
    cols = st.columns(cols_per_row)
    for j, item in enumerate(items[i : i + cols_per_row]):
        with cols[j]:
            name = item["name"]
            ticker = item["ticker"]
            data = item["data"]
            zscore = item["zscore"]

            if data.empty:
                st.write(f"No data available for {name} ({ticker})")
            else:
                fig, ax = plt.subplots(figsize=(4, 3))
                ax.plot(data.index, data["Close"], label="Close", linewidth=1)
                # Label includes name, ticker, and z‑score
                ax.set_title(f"{name} ({ticker})\nz = {zscore:.2f}", fontsize=9)
                ax.tick_params(axis="x", labelrotation=45, labelsize=6)
                ax.tick_params(axis="y", labelsize=6)
                ax.set_xlabel("")
                ax.set_ylabel("")
                plt.tight_layout()
                st.pyplot(fig)
