import tempfile
import time
import unittest
from threading import Event

from pubsub import pub

from src.entry import Entry
from src.monitoring.parser import LogEntryMonitoring
from src.utils.topic import TopicUtils


class TestLogEntryMonitoring(unittest.TestCase):
    def tearDown(self):
        pub.unsubAll()

    def test_new_entry_event_fired(self):
        def on_new_entry_event(entry):
            self.assertIsInstance(entry, Entry)
            event.set()

        tmp = tempfile.NamedTemporaryFile()
        instance = LogEntryMonitoring(publisher=pub, file_path=tmp.name)

        pub.subscribe(on_new_entry_event, TopicUtils.NEW_ENTRY_TOPIC)

        event = Event()
        instance.start()

        time.sleep(0.25)
        tmp.write(b'127.0.0.1 - - [01/Jan/1970:00:00:00 +0000] "GET / HTTP/1.1" 200 1337')
        tmp.seek(0)

        while not event.wait(1):
            self.fail('The timeout period elapsed.')

    def test_parse_line(self):
        line = '127.0.0.1 - - [01/Jan/1970:00:00:00 +0000] "GET / HTTP/1.1" 200 1337'
        entry = Entry(remote_host='127.0.0.1', timestamp=0, method='GET', url='/', status=200, size=1337)

        self.assertTrue(LogEntryMonitoring.parse_line(line) == entry)
