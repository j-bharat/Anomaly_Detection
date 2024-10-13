import matplotlib.pyplot as plt
import time

def continuous_data_stream(data_points, delay=0.01):
    """
    Simulate a continuous data stream from a list of data points.

    Args:
        data_points (list): List of data points to stream.
        delay (float): Delay in seconds between data points.

    Yields:
        float: Next data point in the stream.
    """
    for point in data_points:
        yield point
        time.sleep(delay)  # Simulate real-time streaming delay

def real_time_visualization(data_stream, sdo_stream, stream_length=1000, plot_update_interval=100):
    """Real-time visualization of data stream with detected anomalies."""
    plt.ion()  # Turn on interactive mode for live updating of the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    data_points = []
    anomalies = []

    for idx, data_point in enumerate(data_stream, 1):
        data_points.append(data_point)
        if sdo_stream.detect_anomaly(data_point):
            anomalies.append(idx - 1)

        # Update the plot at specified intervals for better performance
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
            plt.pause(0.001)  # Brief pause to allow plot updates

        # Periodically update observers to adapt to new data trends
        if idx % 500 == 0:
            recent_data = data_points[-200:]
            if len(recent_data) >= 200:
                sdo_stream.update_observers(recent_data)

        # Stop after a fixed length for this example
        if idx >= stream_length:
            break

    plt.ioff()  # Turn off interactive mode
    plt.show()