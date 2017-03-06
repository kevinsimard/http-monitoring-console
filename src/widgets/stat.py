import curses
import math
import time


class StatWindow:
    def __init__(self, window, file, threshold, duration_s, refresh_s):
        self.window = window
        self.file = file
        self.threshold = threshold
        self.duration_s = duration_s
        self.refresh_s = refresh_s

        self.start = time.time()
        self.max_y, self.max_x = window.getmaxyx()

    def render(self, count):
        self.window.erase()

        self._render_header()
        self._render_uptime()
        self._render_total_entry_count(count)
        self._render_threshold()
        self._render_section_expiration()
        self._render_section_refresh()
        self._render_file_path()

        self.window.refresh()

    def _render_header(self):
        self.window.addstr(0, 0, '----- General Stats '.ljust(self.max_x, '-'), curses.A_BOLD)

    def _render_uptime(self):
        m, s = divmod(math.floor(time.time() - self.start), 60)
        h, m = divmod(m, 60)

        self.window.addstr(1, 0, ' Uptime: '.ljust(30))
        self.window.addstr(1, 31, '%d:%02d:%02d' % (h, m, s))

    def _render_threshold(self):
        self.window.addstr(2, 0, ' Threshold Value: '.ljust(30))
        self.window.addstr(2, 31, '%d' % self.threshold)

    def _render_section_expiration(self):
        self.window.addstr(3, 0, ' Section Expiration: '.ljust(30))
        self.window.addstr(3, 31, '%d secs' % self.duration_s)

    def _render_section_refresh(self):
        self.window.addstr(4, 0, ' Section Refresh: '.ljust(30))
        self.window.addstr(4, 31, '%d secs' % self.refresh_s)

    def _render_file_path(self):
        self.window.addstr(5, 0, ' Access Log Path: '.ljust(30))
        self.window.addstr(5, 31, '%s' % self.file)

    def _render_total_entry_count(self, count):
        self.window.addstr(6, 0, ' Total Parsed Log: '.ljust(30))
        self.window.addstr(6, 31, '%d' % count)
