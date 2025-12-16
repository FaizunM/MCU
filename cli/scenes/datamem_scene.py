from cli.scenes import BaseScene
import  curses


class DataMemScene(BaseScene):
    def __init__(self, title, mcu):
        self.title = title

        self.mcu = mcu

        self.offset = 0x0

    def draw(self, stdscr):
        self.data = self.mcu.data_memory.memory
        stdscr.box()
        stdscr.addstr(0, 2, f" {self.title} ")

        h, w = stdscr.getmaxyx()

        self.pos_y = h - 5

        row = self.pos_y if self.pos_y > 8 // len(self.data) else 8 // len(self.data)
        stdscr.addstr(1, 3, "Offset")

        for num in range(0, row):
            stdscr.addstr(num + 3, 3, f"{(num + self.offset) * 16:08x}")

        stdscr.addstr(1, 15, "  ".join(f"{x:02X}" for x in range(16)))
        for num in range(0, row):
            for x in range(8):
                try:
                    value = f"{self.data[x + ((num + self.offset) * 8)]:04X}"
                    stdscr.addstr(num + 3, 15 + (x * 8), f"{value[:2]}")
                    stdscr.addstr(num + 3, 15 + (x * 8 + 4), f"{value[2:]}")
                except:
                    pass

        stdscr.addstr(1, 81, "Decode ANSI")
        for num in range(0, row):
            for x in range(8):
                try:
                    value = f"{self.data[x + ((num + self.offset) * 8)]:04X}"
                    try:

                        stdscr.addstr(num + 3, 81 + (x * 8), f"{chr(int(value[:2]))}")
                    except:
                        stdscr.addstr(num + 3, 81 + (x * 8), f"{'.'}")
                    try:
                        stdscr.addstr(
                            num + 3, 81 + (x * 8 + 4), f"{chr(int(value[2:]))}"
                        )
                    except:
                        stdscr.addstr(num + 3, 81 + (x * 8 + 4), f"{'.'}")

                except:
                    pass
        stdscr.noutrefresh()

    def event_listener(self, key):
        if key == curses.KEY_DOWN:
            self.offset = (self.offset + 1) % (
                (len(self.data) // 16) + 2 - self.pos_y
            )
        if key == curses.KEY_UP:
            self.offset = (self.offset - 1) % (
                (len(self.data) // 16) + 2 - self.pos_y
            )

        if self.offset < 0:
            self.offset = 0

        return False
