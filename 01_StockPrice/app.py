import yfinance as yf
import streamlit as st
from datetime import datetime, timedelta
import requests

# Function to fetch current stock price
def get_current_price(tickerSymbol):
    tickerData = yf.Ticker(tickerSymbol)
    tickerInfo = tickerData.info
    return tickerInfo['currentPrice']

# Page title and description
st.write("""
# Simple Stock Price App
This app retrieves the historical closing price, volume, and current price of the chosen stock!
""")

# Sidebar with user inputs
st.sidebar.header('User Input')

# Allow user to input stock ticker symbol
tickerSymbol = st.sidebar.text_input("Enter Stock Ticker Symbol", 'GOOGL')

# Allow user to input start date
start_date = st.sidebar.date_input("Start Date", datetime(2020, 5, 31))

# End date defaults to current date
current_date = datetime.now().date()
end_date = st.sidebar.date_input("End Date", current_date)

try:
    # Fetch historical data using yfinance
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

    # Display closing price chart
    st.subheader(f"Closing Price ({tickerSymbol})")
    st.line_chart(tickerDf['Close'])

    # Display volume chart
    st.subheader(f"Volume ({tickerSymbol})")
    st.line_chart(tickerDf['Volume'])

    # Display current price
    current_price = get_current_price(tickerSymbol)
    st.write(f"**Current Price:** ${current_price:.2f}")

    # Display stock name and ticker symbol
    tickerInfo = tickerData.info
    st.write(f"**Stock Name:** {tickerInfo['longName']} ({tickerSymbol})")

except (ValueError, KeyError, AttributeError):
    st.sidebar.error("Error: Invalid or unsupported stock ticker symbol. Please try again.")
except requests.exceptions.HTTPError as e:
    st.sidebar.error(f"HTTP Error occurred: {e.response.status_code} - {e.response.reason}")
except Exception as e:
    st.sidebar.error(f"An error occurred: {e}")
