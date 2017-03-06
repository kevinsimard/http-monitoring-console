import time
from datetime import datetime


class Entry:
    DATE_FORMAT = '[%d/%b/%Y:%H:%M:%S %z]'

    def __init__(self, remote_host, timestamp, method, url, status, size, remote_user='-', remote_id='-'):
        self.remote_host = remote_host
        self.timestamp = timestamp
        self.method = method
        self.url = url
        self.status = status
        self.size = size
        self.remote_user = remote_user
        self.remote_id = remote_id

        self.section = Entry.extract_section(url)

    def is_expired(self, duration_s):
        return time.time() - self.timestamp > duration_s

    @staticmethod
    def factory(parts):
        timestamp = datetime.strptime(parts.get('time_received'), Entry.DATE_FORMAT).timestamp()

        return Entry(remote_host=parts.get('remote_host'),
                     timestamp=timestamp,
                     method=parts.get('request_method'),
                     url=parts.get('request_url'),
                     status=int(parts.get('status')),
                     size=int(parts.get('response_bytes')),
                     remote_user=parts.get('remote_user', '-'),
                     remote_id=parts.get('remote_logname', '-'))

    @staticmethod
    def extract_section(url):
        if url == '/':
            return url

        return ''.join(['/', url.split('/')[1], '/'])

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
