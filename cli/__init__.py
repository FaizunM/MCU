from cli.scenes.main_scene import MainScene
from cli.scenes.setting import SettingScene
from cli.scenes.progmem_scene import ProgMemScene
from cli.scenes.datamem_scene import DataMemScene
import curses, time


class CLIMonitor:
    def __init__(self, mcu, mcu_clock):
        self.mcu = mcu
        self.mcu_clock = mcu_clock

        self.scenes = [
            MainScene("Main Control", self.mcu),
            DataMemScene("Data Memory", self.mcu),
            ProgMemScene("Program Memory", self.mcu),
            SettingScene("Setting"),
        ]
        self.scene_index = 0

    def current_scene(self):
        return self.scenes[self.scene_index]

    def next_scene(self):
        self.scene_index = (self.scene_index + 1) % len(self.scenes)

    def prev_scene(self):
        self.scene_index = (self.scene_index - 1) % len(self.scenes)

    def draw_tabbar(self, stdscr):
        h, w = stdscr.getmaxyx()

        offset = 0
        for index, m in enumerate(self.scenes):
            text = f" {m.title} "
            mode = curses.A_REVERSE if index == self.scene_index else curses.A_NORMAL
            stdscr.addstr(h - 1, offset + 2, text, mode)
            offset += len(text)

        stdscr.addstr(h - 1, offset + 5, " <-- Navigasi --> ")

    def mainloop(self, stdscr):
        stdscr.nodelay(False)
        stdscr.keypad(True)
        stdscr.timeout(100)
        curses.curs_set(0)

        while True:
            stdscr.erase()

            self.current_scene().draw(stdscr)
            self.draw_tabbar(stdscr)
            stdscr.noutrefresh()

            key = stdscr.getch()
            listener = self.current_scene().event_listener(key)
            if not listener:
                if key == ord("q"):
                    self.mcu_clock.stop()
                    break
                if key in [ord("C"), ord("c")]:
                    # CLOCK
                    self.mcu.PC.cycle()
                if key == curses.KEY_RIGHT:
                    self.next_scene()
                if key == curses.KEY_LEFT:
                    self.prev_scene()

            curses.doupdate()

    def run(self):
        curses.wrapper(self.mainloop)
