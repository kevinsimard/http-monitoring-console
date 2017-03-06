import curses
from collections import Counter


class SectionWindow:
    def __init__(self, window):
        self.window = window

        self.max_y, self.max_x = window.getmaxyx()

    def render(self, entries):
        self.window.erase()

        self._render_header()
        self._render_table(entries)

        self.window.refresh()

    def _render_header(self):
        self.window.addstr(0, 0, '----- Most Hit Sections '.ljust(self.max_x, '-'), curses.A_BOLD)

    def _render_table(self, entries):
        sections = Counter(x.section for x in entries)
        sorted_sections = sorted(sections.items(), key=lambda x: x[1], reverse=True)

        for i, section in enumerate(sorted_sections):
            message = '%s %d' % (section[0].ljust(30), section[1])

            # TODO: Replace window by pad to avoid this kind of logic
            if i >= self.max_y - 2:
                break

            self.window.addstr(i + 1, 0, message.ljust(self.max_x))
