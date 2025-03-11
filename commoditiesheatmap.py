import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Define the commodities and their ticker symbols
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

st.title("Commodity Maximum Price Chart")

# Dropdown menu to select a commodity
selected_commodity = st.selectbox("Select a Commodity", list(COMMODITIES.keys()))

if selected_commodity:
    ticker = COMMODITIES[selected_commodity]
    
    # Fetch the full historical data using yfinance
    data = yf.download(ticker, period="max")
    
    if data.empty:
        st.error(f"No data available for {selected_commodity}.")
    else:
        # Reset the index so that the Date becomes a column
        data = data.reset_index()

        # Convert the Date column to datetime explicitly
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
        data = data.dropna(subset=["Date"])

        # Determine which column to use for closing prices.
        if "Close" in data.columns and data["Close"].notna().all():
            close_column = "Close"
        elif "Adj Close" in data.columns:
            close_column = "Adj Close"
        else:
            st.error("No valid Close or Adjusted Close data available.")
            st.stop()
        
        # Convert the close column to numeric (float) if necessary
        data[close_column] = pd.to_numeric(data[close_column], errors="coerce")
        data = data.dropna(subset=[close_column])
        
        # Compute the maximum "High" price and its corresponding date
        if "High" in data.columns:
            max_price = data["High"].max()
            max_date = data.loc[data["High"].idxmax(), "Date"]
        else:
            st.error("No High price data available.")
            st.stop()
        
        # Create a line chart for the closing price (or adjusted close)
        fig = px.line(data, x="Date", y=close_column, 
                      title=f"{selected_commodity} Price History ({close_column})")
        
        # Add a marker for the maximum high price
        fig.add_scatter(x=[max_date], y=[max_price], mode="markers", 
                        marker=dict(color="red", size=10), name="Max High Price")
        
        # Add an annotation for the maximum price
        fig.add_annotation(
            x=max_date,
            y=max_price,
            text=f"Max: {max_price:.2f}",
            showarrow=True,
            arrowhead=1
        )
        
        st.plotly_chart(fig, use_container_width=True)
