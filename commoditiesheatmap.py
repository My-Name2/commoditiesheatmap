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
    
    if not data.empty:
        # Reset the index to convert the Date index into a column
        data = data.reset_index()
        
        # Compute the maximum "High" price and its date
        max_price = data["High"].max()
        max_date = data.loc[data["High"].idxmax(), "Date"]

        # Create a line chart of the closing prices
        fig = px.line(data, x="Date", y="Close", title=f"{selected_commodity} Price History (Close)")

        # Add a marker for the maximum high price
        fig.add_scatter(x=[max_date], y=[max_price], mode="markers", 
                        marker=dict(color="red", size=10), name="Max Price")

        # Add an annotation to label the max price
        fig.add_annotation(
            x=max_date,
            y=max_price,
            text=f"Max: {max_price:.2f}",
            showarrow=True,
            arrowhead=1
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"No data available for {selected_commodity}.")
