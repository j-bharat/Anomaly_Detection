import streamlit as st
import yfinance as yf

import matplotlib.pyplot as plt
import time
from io import BytesIO
from data_fetcher import fetch_stock_data
from sdo_stream import SDOStream

def continuous_data_stream(data_points, delay=0.01):
    """
    Simulate a continuous data stream from a list of data points.

    Args:
        data_points (list): List of data points to stream.
        delay (float): Delay in seconds between yielding data points (default is 0.01).

    Yields:
        float: The next data point in the stream.
    """
    for point in data_points:
        yield point
        time.sleep(delay)

def real_time_visualization(data_stream, sdo_stream, stream_length=1000, plot_update_interval=100):
    """
    Real-time visualization of data stream with detected anomalies.

    Args:
        data_stream (iterable): An iterable stream of data points.
        sdo_stream (SDOStream): An instance of the SDOStream class for anomaly detection.
        stream_length (int): Total number of data points to stream (default is 1000).
        plot_update_interval (int): How often (in data points) to update the plot (default is 100).
    """
    data_points = []
    anomalies = []
    
    fig, ax = plt.subplots(figsize=(12, 6))
    plot_placeholder = st.empty()

    for idx, data_point in enumerate(data_stream, 1):
        data_points.append(data_point)
        if sdo_stream.detect_anomaly(data_point):
            anomalies.append(idx - 1)

        if idx % plot_update_interval == 0:
            ax.clear()
            ax.plot(data_points, label='Data Stream', color='blue')
            if anomalies:
                anomaly_values = [data_points[i] for i in anomalies]
                anomaly_times = [i for i in anomalies]
                ax.scatter(anomaly_times, anomaly_values, color='red', s=5, label='Anomalies')
            ax.set_xlabel('Time')
            ax.set_ylabel('Adjusted Close Price')
            ax.set_title('Real-time Stock Data Stream with Anomalies')
            ax.legend()
            
            buf = BytesIO()
            fig.savefig(buf, format="png")
            plot_placeholder.image(buf)

        if idx % 500 == 0:
            recent_data = data_points[-200:]
            if len(recent_data) >= 200:
                sdo_stream.update_observers(recent_data)

        if idx >= stream_length:
            break

    plt.close(fig)

def main():
    """
    Main function to run the Streamlit application for stock data anomaly detection.
    
    This function sets up the Streamlit UI components, fetches stock data based on user selection, 
    initializes the anomaly detection model, and starts the real-time data visualization.
    """
    st.title('Stock Data Anomaly Detection using SDO-Stream')

    # List of predefined stock tickers
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'JPM', 'JNJ', 'V']

    # Dropdown for ticker selection
    selected_ticker = st.selectbox('Select a stock ticker:', tickers)

    # Configuration parameters
    data_period = "5y"
    data_interval = "1d"
    stream_length = 1000
    initial_data_window = 200
    delay_between_points = 0.01
    plot_update_interval = 100

    if st.button('Start Analysis'):
        with st.spinner(f'Fetching historical data for {selected_ticker}...'):
            stock_data = fetch_stock_data(selected_ticker, period=data_period, interval=data_interval)
        
        total_data_points = len(stock_data)
        required_data_points = initial_data_window + stream_length

        if total_data_points < required_data_points:
            st.error(f"Not enough data points ({total_data_points}) for the desired stream length ({stream_length}) with an initial data window of {initial_data_window}.")
            st.error("Consider increasing the data period or decreasing the stream length.")
            return

        sdo_stream = SDOStream(num_observers=50, active_observers=5)
        data_gen = continuous_data_stream(stock_data, delay=delay_between_points)

        initial_data = [next(data_gen) for _ in range(initial_data_window)]
        sdo_stream.initialize_observers(initial_data)
        st.success("Observers initialized with initial data window.")

        st.info(f"Starting real-time data stream for {stream_length} data points...")
        real_time_visualization(data_gen, sdo_stream, stream_length=stream_length, plot_update_interval=plot_update_interval)
        st.success("Data stream completed.")

if __name__ == "__main__":
    main()