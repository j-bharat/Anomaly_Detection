# Stock Data Anomaly Detection using SDO-Stream

## Table of Contents
1. [Introduction](#introduction)
2. [Problem Statement](#problem-statement)
3. [Algorithm: SDO-Stream](#algorithm-sdo-stream)
4. [Implementation](#implementation)
5. [Setup](#setup)
6. [Usage](#usage)
7. [Results](#results)
8. [References](#references)

## Introduction

This project implements real-time anomaly detection in stock data streams using the SDO-Stream (Sparse Data Observers Stream) algorithm. It provides a robust solution for identifying unusual patterns in financial time series data.

## Problem Statement

In financial markets, detecting anomalies in stock price movements is crucial for investors, traders, and analysts. Traditional methods often struggle with:

1. The dynamic nature of stock data
2. Handling real-time streams
3. Adapting to concept drift

These challenges can lead to false positives or missed anomalies, potentially resulting in significant financial losses or missed opportunities.

## Algorithm: SDO-Stream

The SDO-Stream algorithm, based on low density models, offers an effective solution for real-time anomaly detection in data streams. It is particularly well-suited for stock market data due to its ability to adapt to changing patterns and handle continuous data streams efficiently.

### Key Features:

1. **Adaptive Observer Pool**: Maintains a set of data observers that dynamically update to reflect recent data trends.
2. **Sparse Representation**: Uses a subset of observers to compute anomaly scores, reducing computational complexity.
3. **Concept Drift Handling**: Periodically updates observers to adapt to evolving data patterns.

### How it Works:

1. Initialize a pool of observers from an initial data window.
2. For each new data point:
   - Compute its distance to the closest observers.
   - Calculate an anomaly score based on these distances.
   - Flag as anomaly if the score exceeds a threshold.
3. Periodically update the observer pool with recent data points.

### Advantages for Stock Data Analysis:

- **Real-time Processing**: Suitable for live stock market data streams.
- **Adaptability**: Adjusts to changing market conditions and trends.
- **Efficiency**: Low computational overhead for quick decision-making.
- **Robustness**: Reduces false positives in volatile market conditions.

## Implementation

Our project implements the SDO-Stream algorithm for real-time anomaly detection in stock price data. Here's an overview of the main components:

1. **Data Fetching** (`data_fetcher.py`): Retrieves historical stock data using the `yfinance` library.
2. **SDO-Stream Algorithm** (`sdo_stream.py`): Implements the core algorithm for anomaly detection.
3. **Real-time Visualization** (`visualization.py`): Provides live plotting of data points and detected anomalies.
4. **Streamlit Web Application** (`main.py`): Offers a user-friendly interface for stock selection and analysis.

## Setup

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/j-bharat/Anomaly_Detection.git
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application:

1. Ensure your virtual environment is activated.
2. Run the Streamlit app:
   ```
   streamlit run main.py
   ```
3. Open the provided URL in your web browser.
4. Select a stock ticker from the dropdown menu.
5. Click "Start Analysis" to begin the real-time anomaly detection process.
6. Observe the live chart showing stock prices and detected anomalies.

## Results

The SDO-Stream algorithm effectively identifies anomalies in stock price movements, adapting to changing market conditions. Anomalies are visually highlighted on the real-time chart, providing immediate insights into unusual price behaviors.


## References

1. Iglesias Vazquez, Felix; Zseby, Tanja; Zimek, Arthur. "Outlier detection based on low density models." University of Southern Denmark.

2. Félix Iglesias Vázquez, Alexander Hartl, Tanja Zseby, Arthur Zimek. "Anomaly detection in streaming data: A comparison and evaluation study."
