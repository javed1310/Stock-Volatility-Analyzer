import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Page config
st.set_page_config(layout="wide")
st.title("📈 Live Stock Market Dashboard")

# Sidebar: Stock input settings
st.sidebar.header("Stock Settings")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, MSFT):", "AAPL")
period = st.sidebar.selectbox("Select Time Period", ["5d", "1mo", "3mo", "6mo", "1y"], index=1)
interval = st.sidebar.selectbox("Select Interval", ["15m", "1h", "1d"], index=1)

# Fetch stock data from Yahoo Finance
data = yf.download(ticker, period=period, interval=interval)

# Show data or error message
st.subheader(f"📊 Data Preview for {ticker}")
if data.empty or len(data) < 3:
    st.warning("⚠️ Not enough data to display. Try increasing the time period or reducing the interval.")
    st.write(data)  # Display what was fetched (even if small)
else:
    st.dataframe(data.tail())  # Show last few records

    # Line chart for Close Price
    st.subheader(f"📈 {ticker} Stock Price Line Chart")
    fig = go.Figure(
        data=go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",  # Ensure it's a line plot
            name="Close Price",
            line=dict(color="cyan", width=2)
        )
    )
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Price (USD)",
        height=500,
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)
