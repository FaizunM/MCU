import curses, time


class ProcessView:
    def __init__(self, h, w, y, x, mcu, title="Proccess Viewer"):
        self.win = curses.newwin(h, w, y, x)
        self.title = title

        self.mcu = mcu
        self.offset = 0x0
        self.pc_pos = 0x0

    def draw(self):
        self.data = self.mcu.program_memory.memory
        self.win.box()
        self.win.addstr(0, 2, f" {self.title} ")
        h, w = self.win.getmaxyx()

        self.pos_y = h - 5

        row = self.pos_y if len(self.data) > self.pos_y else len(self.data)

        self.win.addstr(2, 3, f"Offset [h]")
        for y in range(row):
            if y + self.offset > len(self.data):
                return
            mode = (
                curses.A_REVERSE
                if (y + self.offset) == self.pc_pos
                else curses.A_NORMAL
            )
            self.win.addstr(y + 4, 3, f"{y + self.offset:08X}", mode)

        self.win.addstr(2, 15, f"Instruction")
        for y in range(row):
            try:
                self.win.addstr(y + 4, 15, f"{self.data[(y + self.offset)]:016b}")
            except:
                pass
        self.win.addstr(2, 35, f"Decode")
        for y in range(row):
            try:

                self.win.addstr(
                    y + 4,
                    35,
                    f"{self.mcu.PC.ins_decoder.decode((y + self.offset), self.data[(y + self.offset)], True)}",
                )
            except:
                pass

        self.win.noutrefresh()

    def event_listener(self, key):
        if key in [ord("C"), ord("c")]:
            # CLOCK
            self.offset = self.mcu.PC.counter
        if key in [ord("R"), ord("r")]:
            # REBOOT
            self.offset = self.mcu.PC.counter
        if key == curses.KEY_DOWN:
            self.offset = (self.offset + 1) % (len(self.data) + 1 - self.pos_y)
        if key == curses.KEY_UP:
            self.offset = (self.offset - 1) % (len(self.data) + 1 - self.pos_y)

        return False
