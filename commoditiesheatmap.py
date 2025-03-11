import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.title("SPY Price Chart")

ticker = "SPY"
st.write("Fetching SPY data...")
data = yf.download(ticker, period="max", interval="1d")

if data.empty:
    st.write("No data available for SPY.")
else:
    # Create the matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot the Close price using the DataFrame's index as the date axis
    ax.plot(data.index, data["Close"], label="SPY Close Price")
    ax.set_title("SPY Price History (Close)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Close Price")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Display the matplotlib chart in Streamlit
    st.pyplot(fig)
