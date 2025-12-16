import struct


class ProgramMemory:
    def __init__(self):
        self.memory = [0x0] * 0x4000
        self.application_start = 0x0
        self.application_end = 0x0

        self.bootloader_start = 0x0
        self.bootloader_end = 0x0

    def load_bootloader(self):
        with open("flash.bin", "rb") as f:
            index = 0x0
            while chunk := f.read(2):
                value = struct.unpack("<H", chunk)[0]
                self.memory[index] = value
                index += 1

    def get(self, address):
        if address >= 0x0000 and address <= 0x3FFF:
            return self.memory[address]
        else:
            raise "Out of memory"

    def get_progmem_8bit(self):
        PROGMEM_8bit = []

        for byte in self.memory:
            low = byte & 0xFF
            high = byte >> 8 & 0xFF
            PROGMEM_8bit.append(low)
            PROGMEM_8bit.append(high)

        return PROGMEM_8bit

    def get_data_bus(self, address):
        if address >= 0x0000 and address <= 0x8000:
            PROGMEM = self.get_progmem_8bit()
            return PROGMEM[address]
        else:
            raise "Out of memory"

    def set(self, address, value):
        if address >= 0x0000 and address <= 0x3FFF:
            self.memory[address] = value
        else:
            raise "Out of memory"
