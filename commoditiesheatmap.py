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

def fetch_latest_prices():
    prices = {}
    for commodity, ticker in COMMODITIES.items():
        data = yf.download(ticker, period="1d", interval="1d")
        if not data.empty and "Close" in data.columns:
            prices[commodity] = float(data["Close"].iloc[-1])
    return prices

# Fetch latest prices
st.sidebar.subheader("Fetching Latest Prices...")
prices = fetch_latest_prices()

# Convert prices to DataFrame for heatmap visualization
if prices:
    df = pd.DataFrame(prices.items(), columns=["Commodity", "Latest Price"])
    df = df.sort_values(by="Latest Price", ascending=False)
    fig = px.imshow([df["Latest Price"].values], 
                    labels=dict(x="Commodity", y="", color="Price"),
                    x=df["Commodity"].values, 
                    y=[""],
                    color_continuous_scale="Viridis")
    st.plotly_chart(fig)
    
    # Show Data Table
    st.subheader("Latest Prices")
    st.dataframe(df)
else:
    st.warning("No data available. Please try again later.")
