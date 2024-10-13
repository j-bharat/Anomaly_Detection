import yfinance as yf
import sys

def fetch_stock_data(ticker, period="5y", interval="1d"):
    """
    Fetch historical stock data using yfinance.

    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL').
        period (str): Data period to download (e.g., '5y' for five years).
        interval (str): Data interval (e.g., '1d' for daily).

    Returns:
        list: List of adjusted closing prices in chronological order.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        if hist.empty:
            print(f"No data found for ticker '{ticker}'. Please check the ticker symbol and try again.")
            sys.exit(1)
        # Ensure data is sorted in chronological order
        hist = hist.sort_index()
        adj_close = hist['Close'].tolist()
        return adj_close
    except Exception as e:
        print(f"Error fetching data for ticker '{ticker}': {e}")
        sys.exit(1)