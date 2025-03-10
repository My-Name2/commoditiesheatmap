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
st.title("📈 Commodities Dashboard")

# Sidebar selection
selected_commodity = st.sidebar.selectbox("Select a Commodity", list(COMMODITIES.keys()))

ticker = COMMODITIES[selected_commodity]

def fetch_data(ticker, period="max", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval)
    return data

# Fetch Data
st.sidebar.subheader("Select Time Range")
data = fetch_data(ticker, period="max", interval="1d")

# Display Latest Price
if not data.empty:
    latest_price = data["Close"].iloc[-1]
    st.metric(label=f"{selected_commodity} Latest Price", value=f"${latest_price:.2f}")

    # Plot Price Chart
    fig = px.line(data, x=data.index, y="Close", title=f"{selected_commodity} Price Trend")
    st.plotly_chart(fig)
    
    # Show Data Table
    st.subheader("Historical Prices")
    st.dataframe(data.tail(10))
else:
    st.warning("No data available. Please try a different commodity.")
