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