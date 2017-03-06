import threading
import time
from collections import deque
from threading import Thread

from src.alert import Alert
from src.utils.topic import TopicUtils


class HighTrafficMonitoring(Thread):
    def __init__(self, publisher, threshold, duration_s):
        Thread.__init__(self)
        self.daemon = True

        self.publisher = publisher
        self.threshold = threshold
        self.duration_s = duration_s

        self.entries = deque()
        self.lock = threading.Lock()
        self.alarm_state = False

        self.publisher.subscribe(self._on_new_entry_event, TopicUtils.NEW_ENTRY_TOPIC)

    def run(self):
        while True:
            self.remove_old_entries()

            hits = len(self.entries)

            if not self.alarm_state and hits > self.threshold:
                self._fire_high_traffic_alert_event(hits)
                self.alarm_state = True
            elif self.alarm_state and hits <= self.threshold:
                self._fire_high_traffic_recover_event()
                self.alarm_state = False

            time.sleep(0.25)

    def remove_old_entries(self):
        self.lock.acquire()
        self.entries = [x for x in self.entries if not x.is_expired(self.duration_s)]
        self.lock.release()

    def _on_new_entry_event(self, entry):
        self.lock.acquire()
        self.entries.append(entry)
        self.lock.release()

    def _fire_high_traffic_alert_event(self, hits):
        self.publisher.sendMessage(TopicUtils.HIGH_TRAFFIC_ALERT_TOPIC,
                                   alert=Alert(alert_type=Alert.Type.ALERT, timestamp=time.time(), hits=hits))

    def _fire_high_traffic_recover_event(self):
        self.publisher.sendMessage(TopicUtils.HIGH_TRAFFIC_RECOVER_TOPIC,
                                   alert=Alert(alert_type=Alert.Type.RECOVER, timestamp=time.time()))
