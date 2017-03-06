import time
from enum import Enum


class Alert:
    class Type(Enum):
        ALERT = 1
        RECOVER = 2

    def __init__(self, alert_type, timestamp, hits=None):
        self.alert_type = alert_type
        self.timestamp = timestamp
        self.hits = hits

    def is_expired(self, duration_s):
        return time.time() - self.timestamp > duration_s
