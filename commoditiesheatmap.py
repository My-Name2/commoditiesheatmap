import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.title("Gold Price History (1 Year)")

# Download one year of daily Gold data
data = yf.download("GC=F", period="1y", interval="1d").reset_index()

# Create a matplotlib figure and plot the closing price
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(data["Date"], data["Close"], label="Close Price")
ax.set_title("Gold Price History (1 Year)")
ax.set_xlabel("Date")
ax.set_ylabel("Close Price")
ax.legend()

# Display the plot in the Streamlit app
st.pyplot(fig)
