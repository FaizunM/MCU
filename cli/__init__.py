from board import MCU
from cli.scenes.main_scene import MainScene
from cli.scenes.setting import SettingScene
from cli.scenes.progmem_scene import ProgMemScene
from cli.scenes.datamem_scene import DataMemScene
import curses


class Application:
    def __init__(self):
        self.mcu = MCU()
        self.mcu.run()

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
        curses.curs_set(0)

        while True:
            stdscr.clear()

            self.current_scene().draw(stdscr)
            self.draw_tabbar(stdscr)

            stdscr.refresh()

            try:
                key = stdscr.getch()
                listener = self.current_scene().event_listener(key)
                if not listener:
                    if key in [ord("C"), ord("c")]:
                        # CLOCK
                        self.mcu.PC.cycle()
                    if key in [ord("R"), ord("r")]:
                        # REBOOT
                        self.mcu.run()
                    if key == curses.KEY_RIGHT:
                        self.next_scene()
                    if key == curses.KEY_LEFT:
                        self.prev_scene()
            except KeyboardInterrupt:
                break

    def run(self):
        curses.wrapper(self.mainloop)
