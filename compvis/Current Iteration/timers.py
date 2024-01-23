import numpy as np
from linetimer import CodeTimer


class Timers:
    """
    Timer class to measure execution times of various functions.
    """

    def __init__(self):
        self.timers = {
            "Main Loop": CodeTimer("Main Loop", silent=True),
            "Get Frame": CodeTimer("Get Frame", silent=True),
            "Binary Centroid": CodeTimer("Binary Centroid", silent=True),
            "Show Frame": CodeTimer("Show Frame", silent=True),
            "LSLocalizer": CodeTimer("LSLocalizer", silent=True),
        }
        self.times = {key: [] for key in self.timers}

    def record_time(self, operation):
        self.times[operation].append(self.timers[operation].took)

    def display_averages(self):
        for operation, times in self.times.items():
            avg_time = np.average(times[5:-5]) if times else None
            message = (
                f"The average time for {operation} to execute was {round(avg_time, 5)} ms"
                if avg_time is not None
                else f"No {operation} was timed"
            )
            print(message)


timers = Timers()
