class DataMemory:
    def __init__(self):
        self.memory = [0] * 0x9000
        self.flags = ["C", "Z", "N", "V", "S", "H", "T", "I"]
        
        self.StackPointer = 0x08FF
        
    def get(self, address):
        if address >= 0x0000 and address <= 0x8FFF:
            return self.memory[address]
        else:
            raise "Out of memory"
        
    def set(self, address, value):
        if address >= 0x0000 and address <= 0x8FFF:
            self.memory[address] = value
        else:
            raise "Out of memory"

    def get_SREG(self):
        return self.get_GPIO(0x3F)
    
    def reset_SREG(self):
        self.set_GPIO(0x3F, 0x0)
    
    def get_SREG_bit(self, flag):
        sreg = self.get_GPIO(0x3F)
        return sreg >> self.flags.index(flag) & 0b1

    def set_SREG_bit(self, flag, bit):
        sreg = self.get_GPIO(0x3F)
        pos = self.flags.index(flag)
        if bit:
            shifted = sreg | (1 << pos)
            self.set_GPIO(0x3F, shifted)
        else:
            shifted = sreg & ~(1 << pos)
            self.set_GPIO(0x3F, shifted)
            
    def get_GPR(self, address):
        if address >= 0x0000 and address <= 0x001F:
            return self.memory[address]
        else:
            raise "Out of memory"

    def set_GPR(self, address, value):
        if address >= 0x0000 and address <= 0x001F:
            self.memory[address] = value & 0xFF
        else:
            raise "Out of memory"

    def get_GPIO(self, address):
        offset = address + 0x20
        if offset >= 0x0020 and offset <= 0x005F:
            return self.memory[offset]
        else:
            raise "Out of memory"

    def set_GPIO(self, address, value):
        offset = address + 0x20
        if offset >= 0x0020 and offset <= 0x005F:
            self.memory[offset] = value & 0xFF
        else:
            raise "Out of memory"

    def get_GPEXTIO(self, address):
        offset = address + 0x60
        if offset >= 0x0060 and offset <= 0x00FF:
            return self.memory[offset]
        else:
            raise "Out of memory"

    def set_GPEXTIO(self, address, value):
        offset = address + 0x60
        if offset >= 0x0060 and offset <= 0x00FF:
            self.memory[offset] = value & 0xFF
        else:
            raise "Out of memory"

    def get_SRAM(self, address):
        offset = address + 0x100
        if offset >= 0x0100 and offset <= 0x08FF:
            return self.memory[offset]
        else:
            raise "Out of memory"

    def set_SRAM(self, address, value):
        offset = address + 0x100
        if offset >= 0x0100 and offset <= 0x08FF:
            self.memory[offset] = value & 0xFF
        else:
            raise "Out of memory"

    def get_GPRs(self):
        return self.memory[0x0000:0x0020]

    def get_GPIORs(self):
        return self.memory[0x0020:0x0060]

    def get_GPEXTIORs(self):
        return self.memory[0x0060:0x00100]

    def get_SRAMs(self):
        return self.memory[0x0100:0x08FF]
