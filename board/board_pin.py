class BoardPin:
    def __init__(self, mcu):
        self.mcu = mcu
        self.pin_io = [0] * 32

    def get_pin(self, id):
        return self.pin_io[id]

    def set_pin(self, id, value):
        self.pin_io[id] = value
        
    def DAC(self, bit):
        return bit * 5.0

    def update(self):
        self.set_pin(4, 5.0)
        
        # PORTD
        portd_direction = self.mcu.data_memory.get_GPIO(0x0A)
        portd_output = self.mcu.data_memory.get_GPIO(0x0B)
        portd_input = self.mcu.data_memory.get_GPIO(0x09)
        
        for pd in reversed(range(8)):
            direction = portd_direction >> pd & 0b1
            if direction:
                # OUTPUT
                bit = portd_output >> pd & 0b1
                self.set_pin(31 - pd, self.DAC(bit))
            else:
                # INPUT
                bit = portd_input >> pd & 0b1
                self.set_pin(31 - pd, self.DAC(bit))
        # PORTC
        portc_direction = self.mcu.data_memory.get_GPIO(0x07)
        portc_output = self.mcu.data_memory.get_GPIO(0x08)
        portc_input = self.mcu.data_memory.get_GPIO(0x06)
        
        for pd in reversed(range(6)):
            direction = portc_direction >> pd & 0b1
            if direction:
                # OUTPUT
                bit = portc_output >> pd & 0b1
                self.set_pin(13 - pd, self.DAC(bit))
            else:
                # INPUT
                bit = portc_input >> pd & 0b1
                self.set_pin(13 - pd, self.DAC(bit))
        # PORTB
        portb_direction = self.mcu.data_memory.get_GPIO(0x04)
        portb_output = self.mcu.data_memory.get_GPIO(0x05)
        portb_input = self.mcu.data_memory.get_GPIO(0x03)
        
        for pd in reversed(range(6)):
            direction = portb_direction >> pd & 0b1
            if direction:
                # OUTPUT
                bit = portb_output >> pd & 0b1
                self.set_pin(23 - pd, self.DAC(bit))
            else:
                # INPUT
                bit = portb_input >> pd & 0b1
                self.set_pin(23 - pd, self.DAC(bit))
                
    def reset(self):
        self.pin_io = [0] * 32
        
        self.set_pin(4, 0.0)