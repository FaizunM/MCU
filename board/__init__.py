from gui import MCUBoardView
from board.mcu import MCU
from cli import CLIMonitor
from board.board_power import BoardPower
from board.board_pin import BoardPin
from board.mcu_clock import MCUClock
from board.reset_controller import ResetController
import threading

class MCUBoard:
    def __init__(self):
        self.mcu = MCU()
        self.board_pin = BoardPin(self.mcu)
        self.mcu.init()

        self.board_power = BoardPower()

        self.mcu_clock = MCUClock(self.mcu, self.board_power, self.board_pin)
        self.reset_controller = ResetController(
            self.mcu, self.mcu_clock, self.board_power
        )

        self.cli_mon = CLIMonitor(self.mcu, self.mcu_clock)
        self.cli_mon_thread = threading.Thread(target=self.cli_mon.run, daemon=True)
        self.mcu_clock_thread = threading.Thread(target=self.mcu_clock.run, daemon=True)
        self.rescon_thread = threading.Thread(
            target=self.reset_controller.run, daemon=True
        )

        self.board_view = MCUBoardView(self, self.board_pin)

    def run(self):
        self.cli_mon_thread.start()
        self.mcu_clock_thread.start()
        self.rescon_thread.start()
        self.board_view.run()

        self.board_view.exit()
