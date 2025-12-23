class ProgramCounter:
    def __init__(self, ins_decoder, program_memory):
        self.counter = 0x0
        self.program_memory = program_memory
        self.ins_decoder = ins_decoder

    def cycle(self):
        instruction = self.program_memory.get(self.counter)

        self.counter += 1
        if self.counter >= len(self.program_memory.memory):
            self.counter = 0
        self.ins_decoder.decode(self.counter, instruction)
