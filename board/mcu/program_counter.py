from board.mcu.instruction_decoder import InstructionDecoder


class ProgramCounter:
    def __init__(self, data_memory, program_memory):
        self.counter = 0x0
        self.data_memory = data_memory
        self.program_memory = program_memory

        self.ins_decoder = InstructionDecoder(self, self.program_memory, self.data_memory)
    
    def reset(self):
        self.counter = 0x0
    
    def cycle(self):
        instruction = self.program_memory.get(self.counter)

        self.counter += 1
        self.ins_decoder.decode(self.counter, instruction)
