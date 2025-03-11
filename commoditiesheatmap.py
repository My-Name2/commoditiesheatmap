import streamlit as st
import yfinance as yf
import pandas as pd

st.title("Commodity Price Viewer")

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

# Create a selectbox for choosing a commodity
commodity = st.selectbox("Select a Commodity", list(commodities.keys()))

# Get the corresponding ticker symbol
ticker = commodities[commodity]

st.write("Fetching data for", commodity)
data = yf.download(ticker, period="max", interval="1d").reset_index()

if not data.empty:
    # Optionally, set the Date column as index for better plotting
    data = data.set_index("Date")
    st.line_chart(data["Close"])
    st.write(f"Data from {data.index.min().date()} to {data.index.max().date()}")
else:
    st.write("No data available for", commodity)
