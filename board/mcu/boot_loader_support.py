class LockBits:
    def __init__(self):
        self.blb0 = 0b00
        self.blb1 = 0b00
        
    def BLB0_mode(self):
        if self.blb0 == 0b11:
            return 1
        if self.blb0 == 0b10:
            return 2
        if self.blb0 == 0b01:
            return 3
        if self.blb0 == 0b00:
            return 4
        

    def get_BLB0(self):
        return self.blb0

    def get_BLB1(self):
        return self.blb1

    def set_BLB0(self, mode):
        self.blb0 = mode

    def set_BLB1(self, mode):
        self.blb1 = mode


class FuseMemory:
    def __init__(self):
        self.lfuse = 0b00000000
        self.hfuse = 0b00000111
        self.efuse = 0b00000000

    def get_BOOTRST(self):
        return self.hfuse & 0b1

    def get_BOOTSZ0(self):
        return self.hfuse >> 1 & 0b1

    def get_BOOTSZ1(self):
        return self.hfuse >> 2 & 0b1

    def set_BOOTSZ0(self, bit):
        k = 1
        if bit == 1:
            new = self.hfuse | (1 << k)
        else:
            new = self.hfuse & ~(1 << k)
            self.hfuse = new

    def set_BOOTSZ1(self, bit):
        k = 1
        if bit == 1:
            new = self.hfuse | (1 << k)
        else:
            new = self.hfuse & ~(1 << k)
            self.hfuse = new

class BootLoaderSupport:
    def __init__(self):
        self.fuse = FuseMemory()
        self.lock_bits = LockBits()