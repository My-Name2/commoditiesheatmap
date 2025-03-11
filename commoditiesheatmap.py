import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")  # Use the full width of the browser

st.title("Commodities Dashboard")

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

# Timeframe controls
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

# Cache data to speed up repeated downloads
@st.cache_data
def get_data(ticker, period, interval):
    return yf.download(ticker, period=period, interval=interval)

# How many charts per row
cols_per_row = 3
items = list(dashboard.items())

# Display the charts in a grid
for i in range(0, len(items), cols_per_row):
    cols = st.columns(cols_per_row)
    for j, (name, ticker) in enumerate(items[i : i + cols_per_row]):
        with cols[j]:
            # Fetch data
            data = get_data(ticker, period, interval)
            if data.empty:
                st.write(f"No data available for {name} ({ticker})")
            else:
                fig, ax = plt.subplots(figsize=(4, 3))
                ax.plot(data.index, data["Close"], label="Close", linewidth=1)
                # Add a small title with the commodity name and ticker
                ax.set_title(f"{name} ({ticker})", fontsize=10)
                ax.tick_params(axis="x", labelrotation=45, labelsize=6)
                ax.tick_params(axis="y", labelsize=6)
                ax.set_xlabel("")
                ax.set_ylabel("")
                plt.tight_layout()
                st.pyplot(fig)
