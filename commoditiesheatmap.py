import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

# Initialize the chart counter in session state if it doesn't exist yet.
if "chart_count" not in st.session_state:
    st.session_state.chart_count = 1

st.title("Multi-Chart SPY Viewer")

# Button to add an extra chart (up to 100)
if st.button("Add Chart"):
    if st.session_state.chart_count < 100:
        st.session_state.chart_count += 1
    else:
        st.warning("Maximum of 100 charts reached.")

st.write("Number of charts:", st.session_state.chart_count)

# Loop to create and display each chart
for i in range(st.session_state.chart_count):
    st.subheader(f"Chart {i+1}")
    
    # Download historical data for SPY
    ticker = "SPY"
    data = yf.download(ticker, period="max", interval="1d")
    
    # Create a matplotlib figure for this chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data["Close"], label="SPY Close Price")
    ax.set_title("SPY Price History (Close)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Close Price")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Display the matplotlib figure in Streamlit
    st.pyplot(fig)
