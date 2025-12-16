from cli.scenes import BaseScene
from cli.scenes.widgets.process_view import ProcessView
from cli.scenes.widgets.register_view import RegisterView
import time

class MainScene(BaseScene):
    def __init__(self, title, mcu):
        self.title = title
        self.mcu = mcu

        self.tabbing = []

        self.select_option = 0

    def draw(self, stdscr):
        if len(self.tabbing) < 1:
            h, w = stdscr.getmaxyx()
            self.tabbing.append(ProcessView(h, w // 2, 0, w // 2,self.mcu))
            self.tabbing[0].offset =  self.mcu.PC.counter - 1
            self.tabbing.append(
                RegisterView(
                    h,
                    w // 2,
                    0,
                    w // 2,
                    self.mcu.data_memory.get_GPRs,
                    "GPR Viewer",
                )
            )
            self.tabbing.append(
                RegisterView(
                    h,
                    w // 2,
                    0,
                    w // 2,
                    self.mcu.data_memory.get_GPIORs,
                    "GPIO Viewer",
                )
            )
            self.tabbing.append(
                RegisterView(
                    h,
                    w // 2,
                    0,
                    w // 2,
                    self.mcu.data_memory.get_GPEXTIORs,
                    "EXT GPIO",
                )
            )
            self.tabbing.append(
                RegisterView(
                    h, w // 2, 0, w // 2, self.mcu.data_memory.get_SRAMs, "SRAM"
                )
            )
        self.tabbing[0].pc_pos = self.mcu.PC.counter

        stdscr.box()
        stdscr.addstr(0, 2, f" {self.title} ")
        stdscr.addstr(2, 3, f"Program Counter   : 0x{self.mcu.PC.counter:08X}")

        stdscr.addstr(
            3,
            3,
            f"Application Size  : {self.mcu.program_memory.application_end - self.mcu.program_memory.application_start} word",
        )
        stdscr.addstr(
            4,
            3,
            f"Bootloader Size   : {self.mcu.program_memory.bootloader_end - self.mcu.program_memory.bootloader_start} word",
        )
        stdscr.addstr(
            5, 3, f"SREG              : 0b{self.mcu.data_memory.get_SREG():08b}"
        )

        options = ["Process Viewer", "GPR", "GPIO", "EXT GPIO", "SRAM"]
        for index, option in enumerate(options):
            stdscr.addstr(
                7 + index,
                3,
                f" {'->' if index == self.select_option else '  '} [{index + 1}] {option}",
            )

        stdscr.refresh()

        self.tabbing[self.select_option].draw()

    def event_listener(self, key):
        if key in [ord("1")]:
            self.select_option = 0
            self.tabbing[0].offset = self.tabbing[0].offset
        if key in [ord("2")]:
            self.select_option = 1
            self.tabbing[1].offset = self.tabbing[1].offset
        if key in [ord("3")]:
            self.select_option = 2
            self.tabbing[2].offset = self.tabbing[2].offset
        if key in [ord("4")]:
            self.select_option = 3
            self.tabbing[3].offset = self.tabbing[3].offset
        if key in [ord("5")]:
            self.select_option = 4
            self.tabbing[4].offset = self.tabbing[4].offset

        listener = self.tabbing[self.select_option].event_listener(key)
        
        if not listener:
            return False
        else:
            return True
