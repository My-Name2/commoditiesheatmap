import yfinance as yf
import matplotlib.pyplot as plt
import math
import streamlit as st

# Set up the Streamlit app
st.title("Commodity Price Dashboard")
st.markdown("This dashboard displays historical closing prices for various commodities.")

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

# Dashboard settings: define the number of columns in the grid
cols = 3
num_com = len(commodities)
rows = math.ceil(num_com / cols)

# Create a matplotlib subplots grid
fig, axes = plt.subplots(rows, cols, figsize=(18, rows * 4), sharex=False, sharey=False)
axes = axes.flatten()  # Flatten for easier iteration

# Loop through each commodity and plot its data on a separate subplot
for ax, (name, ticker) in zip(axes, commodities.items()):
    # Download historical data (max available period with daily interval)
    data = yf.download(ticker, period="max", interval="1d").reset_index()
    
    # Ensure the Date column exists (rename the first column if needed)
    if "Date" not in data.columns:
        data = data.rename(columns={data.columns[0]: "Date"})
    
    # Plot the closing prices
    ax.plot(data["Date"], data["Close"], label="Close Price")
    ax.set_title(name)
    ax.set_xlabel("Date")
    ax.set_ylabel("Close Price")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()

# Remove any unused subplots (if the grid has extra axes)
for i in range(len(commodities), len(axes)):
    fig.delaxes(axes[i])

fig.tight_layout()

# Display the matplotlib figure in the Streamlit app
st.pyplot(fig)
