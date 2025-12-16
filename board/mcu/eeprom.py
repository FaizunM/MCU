class EEPROM:
    def __init__(self):
        self.data = [0] * 1024
        
    def get(self, address):
        if address >= 0x0000 and address <= 0x001F:
            return self.data_memory[address]
        else:
            raise "Out of memory"