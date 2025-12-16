import curses


class RegisterView:
    def __init__(self, h, w, y, x, getter, title="Register Viewer"):
        self.win = curses.newwin(h, w, y, x)
        self.title = title

        self.getter = getter
        self.offset = 0x0
        self.pos_y = 0x0

    def draw(self):
        self.win.clear()
        self.data = self.getter()
        self.win.box()
        self.win.addstr(0, 2, f" {self.title} ")
        h, w = self.win.getmaxyx()

        self.pos_y = h - 5

        row = self.pos_y if len(self.data) > self.pos_y else len(self.data)

        self.win.addstr(2, 3, f"Offset [h]")
        for y in range(row):
            self.win.addstr(y + 4, 3, f"{y + self.offset:08x}")

        self.win.addstr(2, 15, f"Value")
        for y in range(row):
            try:
                self.win.addstr(y + 4, 15, f"{self.data[y + self.offset]:08b}")
            except:
                row -= 1
                pass
        
        self.win.addstr(2, 35, f"Hex | Dec")
        for y in range(row):
            self.win.addstr(
                y + 4,
                35,
                f"{self.data[y + self.offset]:04X} | {self.data[y + self.offset]}",
            )
        self.win.refresh()

    def event_listener(self, key):
        if key == curses.KEY_DOWN:
            self.offset = (self.offset + 1) % (len(self.data) + 1 - self.pos_y)
        if key == curses.KEY_UP:
            self.offset = (self.offset - 1) % (len(self.data) + 1 - self.pos_y)

        return False
