import curses
from datetime import datetime

from src.alert import Alert


class AlertWindow:
    def __init__(self, window):
        self.window = window

        self.max_y, self.max_x = window.getmaxyx()

    def render(self, alerts):
        self.window.erase()

        self._render_header()
        self._render_table(alerts)

        self.window.refresh()

    def _render_header(self):
        self.window.addstr(0, 0, '----- High Traffic Alerts '.ljust(self.max_x, '-'), curses.A_BOLD)

    def _render_table(self, alerts):
        for i, alert in enumerate(alerts):
            date = datetime.fromtimestamp(alert.timestamp).strftime('%H:%M:%S')

            if alert.alert_type == Alert.Type.ALERT:
                message = '++ High traffic generated an alert - hits = %d, triggered at %s' % (alert.hits, date)

            elif alert.alert_type == Alert.Type.RECOVER:
                message = '-- High traffic recovered - triggered at %s' % date

            else:
                continue

            # TODO: Replace window by pad to avoid this kind of logic
            if i >= self.max_y - 2:
                break

            self.window.addstr(i + 1, 0, message.ljust(self.max_x))
