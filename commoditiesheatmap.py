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

# Let the user choose a commodity
selected_comm = st.selectbox("Select a Commodity", list(commodities.keys()))
ticker = commodities[selected_comm]

st.write("Fetching data for", selected_comm)
data = yf.download(ticker, period="max", interval="1d").reset_index()

# Flatten the DataFrame columns if they are a MultiIndex.
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

if data.empty:
    st.write("No data available for", selected_comm)
else:
    # Option 1: Using Streamlit's built-in line chart (simple)
    data = data.set_index("Date")
    st.subheader(f"{selected_comm} Close Price")
    st.line_chart(data["Close"])

    # Option 2: Using Plotly Express (with marker for max high)
    # Uncomment the code below if you'd like to use Plotly instead.
    """
    import plotly.express as px

    # Compute maximum high price and corresponding date
    max_price = data["High"].max()
    max_date = data.loc[data["High"].idxmax(), "Date"]

    fig = px.line(data.reset_index(), x="Date", y="Close", title=f"{selected_comm} Price History")
    fig.add_scatter(x=[max_date], y=[max_price],
                    mode="markers",
                    marker=dict(color="red", size=10),
                    name="Max High")
    st.plotly_chart(fig, use_container_width=True)
    """
