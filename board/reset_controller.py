class ResetController:
    def __init__(self, mcu, mcu_clock, board_power):
        self.mcu = mcu
        self.mcu_clock = mcu_clock
        self.board_power = board_power
        self.reset_status = 0x1
        self.last_power = self.board_power.get_5V()

    def get_mcusr(self):
        return self.mcu.data_memory.get_GPIO(0x35)

    def get_PORF(self):
        mcusr = self.get_mcusr()
        return mcusr & 0b1

    def get_EXTRF(self):
        mcusr = self.get_mcusr()
        return mcusr >> 1 & 0b1

    def get_BORF(self):
        mcusr = self.get_mcusr()
        return mcusr >> 2 & 0b1

    def get_WDRF(self):
        mcusr = self.get_mcusr()
        return mcusr >> 3 & 0b1

    def set_PORF(self, bit):
        mcusr = self.get_mcusr()
        k = 0
        if bit == 1:
            new = mcusr | (1 << k)
            self.mcu.data_memory.set_GPIO(0x35, new)
        else:
            new = mcusr & ~(1 << k)
            self.mcu.data_memory.set_GPIO(0x35, new)

    def set_EXTRF(self, bit):
        mcusr = self.get_mcusr()
        k = 1
        if bit == 1:
            new = mcusr | (1 << k)
            self.mcu.data_memory.set_GPIO(0x35, new)
        else:
            new = mcusr & ~(1 << k)
            self.mcu.data_memory.set_GPIO(0x35, new)

    def set_BORF(self, bit):
        mcusr = self.get_mcusr()
        k = 2
        if bit == 1:
            new = mcusr | (1 << k)
            self.mcu.data_memory.set_GPIO(0x35, new)
        else:
            new = mcusr & ~(1 << k)
            self.mcu.data_memory.set_GPIO(0x35, new)

    def set_WDRF(self, bit):
        mcusr = self.get_mcusr()
        k = 3
        if bit == 1:
            new = mcusr | (1 << k)
            self.mcu.data_memory.set_GPIO(0x35, new)
        else:
            new = mcusr & ~(1 << k)
            self.mcu.data_memory.set_GPIO(0x35, new)

    def check(self):
        if self.last_power == 0 and self.board_power.get_5V() > 0.0:
            self.set_PORF(1)
            self.last_power = self.board_power.get_5V()

    def release_POR(self):
        self.set_BORF(0)

    def must_reset(self):
        return self.get_PORF() or self.get_EXTRF() or self.get_WDRF() or self.get_BORF()

    def run(self):
        while True:
            if self.board_power.get_5V() == 0x0:
                self.mcu_clock.is_running = False
                self.mcu.boot_onreset()
            self.check()
            if self.reset_status == 0x0:
                self.mcu_clock.is_running = False
                self.mcu.boot_onreset()
                self.mcu.data_memory.reset_SREG()
                self.release_POR()
            else:
                self.mcu_clock.is_running = True

    def enable_ext_reset(self):
        self.reset_status = 0x0

    def disable_ext_reset(self):
        self.reset_status = 0x1