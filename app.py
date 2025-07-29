import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objs as go
from datetime import date

st.set_page_config(page_title="📈 Stock Volatility Analyzer", layout="wide")

st.title("📊 Stock Price Volatility Analyzer & Risk Estimator")

# Input widgets
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, TSLA):", value="AAPL")
start_date = st.date_input("Start Date", value=date(2022, 1, 1))
end_date = st.date_input("End Date", value=date.today())

@st.cache_data(show_spinner=False)
def fetch_data(ticker, start_date, end_date):
    try:
        df = yf.download(ticker, start=start_date, end=end_date)
        
        # Handle MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            # Convert to flat columns like 'AAPL_Close', 'AAPL_Open', etc.
            df.columns = ['_'.join(col).strip() for col in df.columns.values]
            close_col = [col for col in df.columns if 'Close' in col][0]
            df = df[[close_col]]
            df.rename(columns={close_col: 'Close'}, inplace=True)
        else:
            df = df[["Close"]]

        df.dropna(inplace=True)
        return df
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
        return None

df = fetch_data(ticker, start_date, end_date)

if df is not None and not df.empty:
    st.subheader(f"📉 Close Price of {ticker.upper()} from {start_date} to {end_date}")

    # Price line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Close Price"))
    fig.update_layout(title=f"{ticker.upper()} Stock Closing Price", xaxis_title="Date", yaxis_title="Price (USD)", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # Daily returns
    df["Returns"] = df["Close"].pct_change()
    df = df.dropna()

    # Metrics
    st.subheader("📌 Risk Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Daily Return", f"{df['Returns'].mean():.4%}")
    with col2:
        st.metric("Daily Volatility (Std Dev)", f"{df['Returns'].std():.4%}")
    with col3:
        st.metric("Cumulative Return", f"{(df['Close'].iloc[-1]/df['Close'].iloc[0] - 1):.2%}")

    # Return histogram
    st.subheader("🔍 Return Distribution")
    fig2 = go.Figure()
    fig2.add_trace(go.Histogram(x=df["Returns"], nbinsx=50, marker_color="orange"))
    fig2.update_layout(title="Distribution of Daily Returns", xaxis_title="Daily Return", yaxis_title="Frequency", template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("⚠️ No data to display. Please check the ticker and date range.")
