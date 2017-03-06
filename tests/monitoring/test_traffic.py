import time
import unittest
from threading import Event

from pubsub import pub

from src.alert import Alert
from src.entry import Entry
from src.monitoring.traffic import HighTrafficMonitoring
from src.utils.topic import TopicUtils


class TestHighTraficMonitoring(unittest.TestCase):
    THRESHOLD = 2
    DURATION_S = 1

    def setUp(self):
        self.instance = HighTrafficMonitoring(publisher=pub, threshold=self.THRESHOLD, duration_s=self.DURATION_S)
        self.entry = Entry(remote_host='127.0.0.1', timestamp=time.time(), method='GET', url='/', status=200, size=1337)

    def tearDown(self):
        pub.unsubAll()

    def test_traffic_alert_event_fired(self):
        def on_high_traffic_alert_event(alert):
            self.assertLess(alert.timestamp, time.time())
            self.assertEqual(alert.hits, self.THRESHOLD + 1)
            self.assertEqual(alert.alert_type, Alert.Type.ALERT)
            event.set()

        for _ in range(0, self.THRESHOLD + 1):
            pub.sendMessage(TopicUtils.NEW_ENTRY_TOPIC, entry=self.entry)

        pub.subscribe(on_high_traffic_alert_event, TopicUtils.HIGH_TRAFFIC_ALERT_TOPIC)

        event = Event()
        self.instance.start()

        while not event.wait(1):
            self.fail('The timeout period elapsed.')

    def test_traffic_recovery_event_fired(self):
        def on_high_traffic_recover_event(alert):
            self.assertLess(alert.timestamp, time.time())
            self.assertEqual(alert.hits, None)
            self.assertEqual(alert.alert_type, Alert.Type.RECOVER)
            event.set()

        for _ in range(0, self.THRESHOLD + 1):
            pub.sendMessage(TopicUtils.NEW_ENTRY_TOPIC, entry=self.entry)

        pub.subscribe(on_high_traffic_recover_event, TopicUtils.HIGH_TRAFFIC_RECOVER_TOPIC)

        event = Event()
        self.instance.start()

        while not event.wait(self.DURATION_S + 1):
            self.fail('The timeout period elapsed.')
