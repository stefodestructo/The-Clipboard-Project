#databuffer.py

from datetime import datetime, timedelta

class databuffer:
    buf = []

    def __init__(self, max_time_delta):
        self.max_time_delta = max_time_delta

    def addpoint(self, data_point):
        present_time = datetime.now()
        self.buf.append((present_time, data_point))

    def _timedelta_total_seconds(self, delta):
        return delta.days * 60 * 60  * 24 + delta.seconds + delta.microseconds / 1e6

    def get_buffer(self):
        present_time = datetime.now()
        self.buf = [x for x in self.buf if present_time - x[0] < self.max_time_delta]

        return [(1 - self._timedelta_total_seconds(present_time - x[0]) / self._timedelta_total_seconds(self.max_time_delta), x[1]) \
                for x in self.buf]
