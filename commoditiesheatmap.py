import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Define a comprehensive list of commodities and their ticker symbols
COMMODITIES = {
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
    "Lumber": "LB=F",
    "Live Cattle": "LE=F",
    "Lean Hogs": "HE=F",
    "Feeder Cattle": "GF=F",
    "Oats": "ZO=F",
    "Rough Rice": "ZR=F",
    "Orange Juice": "OJ=F"
}

# Streamlit App Title
st.title("📈 Commodities Heatmap Dashboard")

# ---------- Latest Prices Section ----------
st.sidebar.subheader("Fetching Latest Prices...")

def fetch_latest_prices():
    prices = {}
    for commodity, ticker in COMMODITIES.items():
        data = yf.download(ticker, period="1d", interval="1d")
        if not data.empty and "Close" in data.columns:
            prices[commodity] = float(data["Close"].iloc[-1])
    return prices

# Fetch and display latest prices
prices = fetch_latest_prices()
if prices:
    df_latest = pd.DataFrame(prices.items(), columns=["Commodity", "Latest Price"])
    df_latest = df_latest.sort_values(by="Latest Price", ascending=False)
    
    # Heatmap for latest prices
    fig_latest = px.imshow([df_latest["Latest Price"].values], 
                           labels=dict(x="Commodity", y="", color="Price"),
                           x=df_latest["Commodity"].values, 
                           y=[""],
                           color_continuous_scale="Viridis")
    st.plotly_chart(fig_latest)
    
    st.subheader("Latest Prices")
    st.dataframe(df_latest)
else:
    st.warning("No latest price data available. Please try again later.")

# ---------- Historical Max Prices Section ----------
st.sidebar.subheader("Historical Max Prices Settings")
use_custom_date = st.sidebar.checkbox("Use custom start date for historical data", value=False)
if use_custom_date:
    start_date = st.sidebar.date_input("Select start date", value=pd.to_datetime("2010-01-01"))
else:
    start_date = None  # This will fetch full available history

def fetch_historical_max(start_date=None):
    max_prices = {}
    for commodity, ticker in COMMODITIES.items():
        # If a start date is provided, use it; otherwise, fetch the full history
        if start_date:
            data = yf.download(ticker, start=start_date)
        else:
            data = yf.download(ticker, period="max")
        if not data.empty and "High" in data.columns:
            max_prices[commodity] = float(data["High"].max())
    return max_prices

st.sidebar.subheader("Fetching Historical Max Prices...")
historical_max_prices = fetch_historical_max(start_date)
if historical_max_prices:
    df_max = pd.DataFrame(historical_max_prices.items(), columns=["Commodity", "Max Historical Price"])
    df_max = df_max.sort_values(by="Max Historical Price", ascending=False)
    
    # Heatmap for historical max prices
    fig_max = px.imshow([df_max["Max Historical Price"].values], 
                        labels=dict(x="Commodity", y="", color="Price"),
                        x=df_max["Commodity"].values, 
                        y=[""],
                        color_continuous_scale="Viridis")
    st.plotly_chart(fig_max)
    
    st.subheader("Max Historical Prices")
    st.dataframe(df_max)
else:
    st.warning("No historical max price data available. Please try again later.")
