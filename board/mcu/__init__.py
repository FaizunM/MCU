from board.mcu.boot_loader_support import BootLoaderSupport
from board.mcu.program_counter import ProgramCounter
from board.mcu.program_memory import ProgramMemory
from board.mcu.data_memory import DataMemory
from board.mcu.instruction_decoder import InstructionDecoder
from board.mcu.alu import ALU

class MCU:
    def __init__(self):
        self.bls = BootLoaderSupport()
        self.program_memory = ProgramMemory()     
        self.data_memory = DataMemory()     
        self.ins_decoder = InstructionDecoder(self.program_memory)
        self.PC = ProgramCounter(self.ins_decoder, self.program_memory)
        self.ALU = ALU(self.PC, self.program_memory, self.data_memory, self.bls)
        self.ins_decoder.set_ALU(self.ALU)
        
    def boot(self):
        # BOOT Size Configuration
        bootsz1 = self.bls.fuse.get_BOOTSZ1()
        bootsz0 = self.bls.fuse.get_BOOTSZ0()

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
            
        self.boot_onreset()
           
    def boot_onreset(self):
        # Cek BOOTRST; 1 = normal; 0 = lompat ke bootloader
        if self.bls.fuse.get_BOOTRST():
            self.PC.counter = 0x0
        else:
            self.PC.counter = self.program_memory.bootloader_start

    def init(self):
        self.boot()
        self.program_memory.load_bootloader()