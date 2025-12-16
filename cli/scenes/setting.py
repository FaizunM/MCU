from cli.scenes import BaseScene

class SettingScene(BaseScene):
    def __init__(self, title):
        self.title = title

    def draw(self, stdscr):
        stdscr.box()
        stdscr.addstr(0, 2, f" {self.title} ")
        stdscr.noutrefresh()

    def event_listener(self, key):
        return False