import streamlit as st
import yfinance as yf
import altair as alt
import pandas as pd

st.title("Commodities Dashboard")

# Default commodities dictionary
default_commodities = {
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

# Let users select which default commodities to display
selected = st.multiselect(
    "Select commodities to display",
    options=list(default_commodities.keys()),
    default=list(default_commodities.keys())
)

# Allow users to add additional tickers (comma-separated)
custom_input = st.text_input("Enter additional ticker symbols (comma-separated)", value="")
custom_tickers = [t.strip() for t in custom_input.split(",") if t.strip()]

# Build the dashboard dictionary: display name -> ticker symbol.
dashboard = {}
for name in selected:
    dashboard[name] = default_commodities[name]
for ticker in custom_tickers:
    dashboard[ticker] = ticker  # For custom tickers, the name is the ticker

st.write("Displaying charts for:", list(dashboard.keys()))

# Cache data download for performance.
@st.cache(allow_output_mutation=True)
def get_data(ticker):
    data = yf.download(ticker, period="max", interval="1d")
    data.reset_index(inplace=True)  # So that 'Date' becomes a column
    return data

# Use session state to track the expanded chart.
if "expanded_chart" not in st.session_state:
    st.session_state.expanded_chart = None

def expand_chart(ticker):
    st.session_state.expanded_chart = ticker

# Grid settings: 5 columns per row.
cols_per_row = 5
dashboard_items = list(dashboard.items())

# Display the mini charts in a grid.
for i in range(0, len(dashboard_items), cols_per_row):
    cols = st.columns(cols_per_row)
    for j, (name, ticker) in enumerate(dashboard_items[i : i + cols_per_row]):
        with cols[j]:
            st.subheader(name)
            data = get_data(ticker)
            # Create a small Altair line chart (mini chart)
            mini_chart = alt.Chart(data).mark_line().encode(
                x=alt.X('Date:T', axis=alt.Axis(labels=False, title=None)),
                y=alt.Y('Close:Q', axis=alt.Axis(labels=False, title=None))
            ).properties(width=150, height=100)
            st.altair_chart(mini_chart, use_container_width=True)
            # Expand button for each chart.
            if st.button("Expand", key=f"expand_{ticker}", on_click=expand_chart, args=(ticker,)):
                pass  # The callback sets st.session_state.expanded_chart

# If an expanded chart is selected, show an interactive version below.
if st.session_state.expanded_chart is not None:
    st.markdown("---")
    st.header(f"Expanded Chart for {st.session_state.expanded_chart}")
    exp_data = get_data(st.session_state.expanded_chart)
    # Create an interactive Altair chart (with pan and zoom)
    exp_chart = alt.Chart(exp_data).mark_line().encode(
        x=alt.X('Date:T', title="Date"),
        y=alt.Y('Close:Q', title="Close Price")
    ).properties(
        width=700,
        height=400,
        title=f"{st.session_state.expanded_chart} Price History"
    ).interactive()  # This enables zooming and panning
    st.altair_chart(exp_chart, use_container_width=True)
    if st.button("Close Expanded Chart"):
        st.session_state.expanded_chart = None
