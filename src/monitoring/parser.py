import time
from threading import Thread

import apache_log_parser
from apache_log_parser import LineDoesntMatchException

from src.entry import Entry
from src.utils.topic import TopicUtils


class LogEntryMonitoring(Thread):
    PARSER = apache_log_parser.make_parser('%h %u %l %t "%r" %s %B')

    def __init__(self, publisher, file_path):
        Thread.__init__(self)
        self.daemon = True

        self.publisher = publisher
        self.file_path = file_path

    def run(self):
        file = open(self.file_path, 'r')
        file.seek(0, 2)

        while True:
            line = file.readline()

            if not line.strip():
                time.sleep(0.25)
                continue

            try:
                entry = self.parse_line(line)
                self._fire_new_entry_event(entry)
            except LineDoesntMatchException:
                pass

    @staticmethod
    def parse_line(line):
        parts = LogEntryMonitoring.PARSER(line)

        return Entry.factory(parts)

    def _fire_new_entry_event(self, entry):
        self.publisher.sendMessage(TopicUtils.NEW_ENTRY_TOPIC, entry=entry)
