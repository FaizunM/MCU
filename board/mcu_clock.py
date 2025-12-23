import time

class MCUClock:
    def __init__(self, mcu, board_power, board_pin):
        self.mcu = mcu
        self.is_running = False
        self.board_power = board_power
        self.board_pin = board_pin

    def run(self):
        while True:
            if self.board_power.get_5V() > 4.3:
                self.board_pin.update()
            else:
                self.board_pin.reset()
            if self.is_running and self.board_power.get_5V() > 4.3:
                self.mcu.PC.cycle()
            time.sleep(0.1)

    def stop(self):
        self.is_running = False
