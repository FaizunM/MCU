from application.board_view import MCUBoardView
from board import MCU
import threading, time
from multiprocessing import Process
from cli import CLIMonitor
import queue


class MCUClock:
    def __init__(self, mcu):
        self.mcu = mcu
        self.is_running = threading.Event()
        self.is_running.set()
        
    def run(self):
        while self.is_running.is_set():
            self.mcu.PC.cycle()
            time.sleep(1)

    def stop(self):
        self.is_running.clear()


class MCUBoard:
    def __init__(self):
        self.mcu = MCU()
        self.mcu.setup()

        self.power = 0x1
        self.V5Power, self.V3_3Power = self.get_voltage(self.power)

        self.mcu_clock = MCUClock(self.mcu)

        self.cli_mon = CLIMonitor(self.mcu, self.mcu_clock)
        self.cli_mon_thread = threading.Thread(target=self.cli_mon.run)
        self.mcu_clock_thread = threading.Thread(target=self.mcu_clock.run, daemon=True)
        
        self.cli_mon_thread.start()
        self.mcu_clock_thread.start()

    def get_voltage(self, power):
        if power:
            return 5.0, 3.3
        else:
            return 0.0, 0.0

    def plug_power(self):
        self.power = 0x1

    def unplug_power(self):
        self.power = 0x0

    def run(self):
        self.board_view = MCUBoardView(self)
        self.board_view.run()
        self.board_view.exit()
        self.mcu_clock.stop()
