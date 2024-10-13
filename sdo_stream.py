import numpy as np
import random
from collections import deque

class SDOStream:
    def __init__(self, num_observers=50, active_observers=5, idle_threshold=0.3):
        """
        Initialize the SDOStream object.

        Args:
            num_observers (int): Total number of observers in the model.
            active_observers (int): Number of closest observers used to compute outlier score.
            idle_threshold (float): Threshold to remove idle observers.
        """
        self.num_observers = num_observers
        self.active_observers = active_observers
        self.idle_threshold = idle_threshold
        self.observers = deque(maxlen=self.num_observers)  # FIFO structure for observers

    def initialize_observers(self, data_window):
        """Initialize observers randomly from a batch of data points."""
        self.observers = deque(random.sample(data_window, min(len(data_window), self.num_observers)), maxlen=self.num_observers)

    def update_observers(self, new_data):
        """Update observers with new data points to adapt to concept drift."""
        num_to_replace = int(self.num_observers * 0.2)
        new_observers = random.sample(new_data, min(len(new_data), num_to_replace))
        for observer in new_observers:
            if len(self.observers) >= self.num_observers:
                self.observers.popleft()
            self.observers.append(observer)

    def compute_outlier_score(self, data_point):
        """Calculate the outlier score based on distance to the closest observers."""
        observer_array = np.array(self.observers)
        distances = np.abs(observer_array - data_point)
        closest_distances = np.partition(distances, self.active_observers)[:self.active_observers]
        outlier_score = np.median(closest_distances)
        return outlier_score

    def detect_anomaly(self, data_point, threshold=25):
        """Flag an anomaly if the outlier score exceeds a threshold."""
        score = self.compute_outlier_score(data_point)
        return score > threshold