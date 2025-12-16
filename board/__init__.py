from board.mcu.fuse_memory import FuseMemory
from board.mcu.program_counter import ProgramCounter
from board.mcu.program_memory import ProgramMemory
from board.mcu.data_memory import DataMemory

class MCU:
    def __init__(self):
        self.message = None
        self.fuse_memory = FuseMemory()
        
        self.program_memory = ProgramMemory()     
        self.data_memory = DataMemory()     
        self.PC = ProgramCounter(self.data_memory, self.program_memory)
        
    def boot(self):
        # BOOT Size Configuration
        bootsz1 = self.fuse_memory.get_BOOTSZ1()
        bootsz0 = self.fuse_memory.get_BOOTSZ0()
        

        if bootsz1 == 0b1 and bootsz0 == 0b1:
            self.program_memory.application_start = 0x0000
            self.program_memory.application_end = 0x3EFF

            self.program_memory.bootloader_start = 0x3F00
            self.program_memory.bootloader_end = 0x3FFF

        if bootsz1 == 0b1 and bootsz0 == 0b0:
            self.program_memory.application_start = 0x0000
            self.program_memory.application_end = 0x3DFF

            self.program_memory.bootloader_start = 0x3E00
            self.program_memory.bootloader_end = 0x3FFF            

        if bootsz1 == 0b0 and bootsz0 == 0b1:
            self.program_memory.application_start = 0x0000
            self.program_memory.application_end = 0x3BFF

            self.program_memory.bootloader_start = 0x3C00
            self.program_memory.bootloader_end = 0x3FFF

        if bootsz1 == 0b0 and bootsz0 == 0b0:
            self.program_memory.application_start = 0x0000
            self.program_memory.application_end = 0x37FF

            self.program_memory.bootloader_start = 0x3800
            self.program_memory.bootloader_end = 0x3FFF
            

        # Cek BOOTRST; 1 = normal; 0 = lompat ke bootloader
        if self.fuse_memory.get_BOOTRST():
            self.PC.counter = 0x0
        else:
            self.PC.counter = self.program_memory.bootloader_start

    def setup(self):
        self.boot()
        self.program_memory.load_bootloader()