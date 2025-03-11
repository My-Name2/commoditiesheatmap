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

st.title("📈 Commodities Dashboard")

# ---------- Latest Prices Section (Existing Code) ----------
st.sidebar.subheader("Fetching Latest Prices...")

def fetch_latest_prices():
    prices = {}
    for commodity, ticker in COMMODITIES.items():
        data = yf.download(ticker, period="1d", interval="1d")
        if not data.empty and "Close" in data.columns:
            prices[commodity] = float(data["Close"].iloc[-1])
    return prices

prices = fetch_latest_prices()
if prices:
    df_latest = pd.DataFrame(prices.items(), columns=["Commodity", "Latest Price"])
    df_latest = df_latest.sort_values(by="Latest Price", ascending=False)
    
    # Display latest prices heatmap for reference (optional)
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

# ---------- Price Return Section ----------
st.sidebar.subheader("Price Return Settings")
price_return_start_date = st.sidebar.date_input("Select start date for price return", value=pd.to_datetime("2010-01-01"))

def fetch_price_return(start_date):
    returns = {}
    for commodity, ticker in COMMODITIES.items():
        data = yf.download(ticker, start=start_date)
        if not data.empty and "Close" in data.columns:
            start_price = data["Close"].iloc[0]
            latest_price = data["Close"].iloc[-1]
            # Calculate percentage return
            returns[commodity] = ((latest_price / start_price) - 1) * 100
    return returns

price_returns = fetch_price_return(price_return_start_date)
if price_returns:
    df_return = pd.DataFrame(price_returns.items(), columns=["Commodity", "Return"])
    df_return = df_return.sort_values(by="Return", ascending=False)
    
    # Create a bar chart with a diverging color scale (red for negative, green for positive)
    fig_return = px.bar(
        df_return,
        x="Commodity",
        y="Return",
        color="Return",
        color_continuous_scale="RdYlGn",
        title=f"Price Return (%) since {price_return_start_date.strftime('%Y-%m-%d')}"
    )
    st.plotly_chart(fig_return)
    
    st.subheader("Price Returns Data")
    st.dataframe(df_return)
else:
    st.warning("No price return data available. Please try again later.")
