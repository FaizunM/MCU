class SPIStatusRegister:
    def __init__(self):
        pass


class SPIControlRegister:
    def __init__(self):
        pass


class SPI:
    def __init__(self):
        self.active = False
        
    def run(self, mosi, miso, sck, ss):
        if ss == 0x0:
            self.active = True
