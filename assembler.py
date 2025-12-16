import struct


class Assembler:
    def __init__(self, pathfile, save_path):
        self.pathfile = pathfile
        self.save_path = save_path

        self.pattern_list = {
            "ADC": "000111rdddddrrrr",
            "ADD": "000011rdddddrrrr",
            "ADIW": "10010110KKddKKKK",
            "AND": "001000rdddddrrrr",
            "ANDI": "0111KKKKddddKKKK",
            "ASR": "1001010ddddd0101",
            "BCLR": "100101001sss1000",
            "BLD": "1111100ddddd0bbb",
            "BRBC": "111101kkkkkkksss",
            "BRBS": "111100kkkkkkksss",
            "BRCC": "111101kkkkkkk000",
            "BRCS": "111100kkkkkkk000",
            "BREAK": "1001010110011000",
            "BREQ": "111100kkkkkkk001",
            "BRGE": "111101kkkkkkk100",
            "BRHC": "111101kkkkkkk100",
            "BRHS": "111100kkkkkkk101",
            "BRID": "111101kkkkkkk111",
            "BRIE": "111100kkkkkkk111",
            "BRLO": "111100kkkkkkk000",
            "BRLT": "111100kkkkkkk100",
            "BRMI": "111100kkkkkkk010",
            "BRNE": "111101kkkkkkk001",
            "BRPL": "111101kkkkkkk010",
            "BRSH": "111101kkkkkkk000",
            "BRTC": "111101kkkkkkk110",
            "BRTS": "111100kkkkkkk110",
            "BRVC": "111101kkkkkkk011",
            "BRVS": "111100kkkkkkk011",
            "BSET": "100101000sss1000",
            "BST": "1111101ddddd0bbb",
            "CALL": "1001010kkkkk111kkkkkkkkkkkkkkkkk",
            "CBI": "10011000AAAAAbbb",
            "CLC": "1001010010001000",
            "CLH": "1001010011011000",
            "CLI": "1001010011111000",
            "CLN": "1001010010101000",
            "CLR": "001001dddddddddd",
            "CLS": "1001010011001000",
            "CLT": "1001010011101000",
            "CLV": "1001010010111000",
            "CLZ": "1001010010011000",
            "COM": "1001010ddddd0000",
            "CP": "000101rdddddrrrr",
            "CPC": "000001rdddddrrrr",
            "CPI": "0011KKKKddddKKKK",
            "CPSE": "000100rdddddrrrr",
            "DEC": "1001010ddddd1010",
            "DES": "10010100KKKK1011",
            "EICALL": "1001010100011001",
            "EIJMP": "1001010000011001",
            "ELPM": "1001010111011000",
            "EOR": "001001rdddddrrrr",
            "FMUL": "000000110ddd1rrr",
            "FMULS": "000000111ddd0rrr",
            "FMULSU": "000000111ddd1rrr",
            "ICALL": "1001010100001001",
            "IJMP": "1001010000001001",
            "IN": "10110AAdddddAAAA",
            "INC": "1001010ddddd0011",
            "JMP": "1001010kkkkk110kkkkkkkkkkkkkkkkk",
            "LAC": "1001001rrrrr0110",
            "LAS": "1001001rrrrr0101",
            "LAT": "1001001rrrrr0111",
            "LD": "1001000ddddd1100",
            "LDI": "1110KKKKddddKKKK",
            "LDS": "1001000ddddd0000kkkkkkkkkkkkkkkk",
            "LPM": "1001010111001000",
            "LSL": "000011dddddddddd",
            "LSR": "1001010ddddd0110",
            "MOV": "001011rdddddrrrr",
            "MOVW": "00000001ddddrrrr",
            "MUL": "100111rdddddrrrr",
            "MULS": "00000010ddddrrrr",
            "MULSU": "000000110ddd0rrr",
            "NEG": "1001010ddddd0001",
            "NOP": "0000000000000000",
            "OR": "001010rdddddrrrr",
            "ORI": "0110KKKKddddKKKK",
            "OUT": "10111AArrrrrAAAA",
            "POP": "1001000ddddd1111",
            "PUSH": "1001001ddddd1111",
            "RCALL": "1101kkkkkkkkkkkk",
            "RET": "1001010100001000",
            "RETI": "1001010100011000",
            "RJMP": "1100kkkkkkkkkkkk",
            "ROL": "000111dddddddddd",
            "ROR": "1001010ddddd0111",
            "SBC": "000010rdddddrrrr",
            "SBCI": "0100KKKKddddKKKK",
            "SBI": "10011010AAAAAbbb",
            "SBIC": "10011001AAAAAbbb",
            "SBIS": "10011011AAAAAbbb",
            "SBIW": "10010111KKddKKKK",
            "SBR": "0110KKKKddddKKKK",
            "SBRC": "1111110rrrrr0bbb",
            "SBRS": "1111111rrrrr0bbb",
            "SEC": "1001010000001000",
            "SEH": "1001010001011000",
            "SEI": "1001010001111000",
            "SEN": "1001010000101000",
            "SER": "11101111dddd1111",
            "SES": "1001010001001000",
            "SET": "1001010001101000",
            "SEV": "1001010000111000",
            "SEZ": "1001010000011000",
            "SLEEP": "1001010110001000",
            "SPM": "1001010111101000",
            "ST": "1001001rrrrr1100",
            "STS": "1001001ddddd0000kkkkkkkkkkkkkkkk",
            "SUB": "000110rdddddrrrr",
            "SUBI": "0101KKKKddddKKKK",
            "SWAP": "1001010ddddd0010",
            "TST": "001000dddddddddd",
            "WDR": "1001010110101000",
            "XCH": "1001001rrrrr0100",
        }

        self.XYZ_registers = {"X": "1100", "X+": "1101", "-X": "1110"}

        self.counter = 0x0
        self.PC = 0x0
        self.labels = {}
        self.symbols = {}

    def read(self):
        with open(self.pathfile, "r") as f:
            lines = f.readlines()
            f.close()
            return lines

    def get_opcode(self, line):
        return line[0]

    def get_operands(self, line):
        operands = []
        if len(line) > 1:
            operands = [op.strip() for op in line[1].split(",")]
        return operands

    def clear_line(self, line):
        # remove comment
        line = line.split(";")[0].strip()
        line = line.split(None, 1)
        # remove enter
        if not line:
            return None
        return line

    def encode(self, line):
        syntax = self.clear_line(line)
        if syntax == None:
            return None

        opcode = self.get_opcode(syntax).upper()
        operands = self.get_operands(syntax)

        if opcode in [
            "ADIW",
        ]:
            pattern = self.pattern_list[opcode]

            destination = f"{int(operands[0][1:]) - 24:04b}"
            data = f"{int(operands[1], 16):06b}"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "d" else c for c in pattern)
            it = iter(data)
            replace2 = "".join(next(it) if c == "K" else c for c in replace1)
            return replace2

        if opcode in [
            "ANDI",
            "CPI",
            "LDI",
            "ORI",
            "SBCI",
            "SBR",
            "SUBI",
            "CBR",
        ]:
            pattern = self.pattern_list[opcode]

            if int(operands[0][1:]) < 16:
                raise "Only R16-R31 accessible"

            destination = f"{int(operands[0][1:]) - 16:04b}"
            data = f"{int(operands[1], 16) & 0xFF:08b}"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "d" else c for c in pattern)
            it = iter(data)
            replace2 = "".join(next(it) if c == "K" else c for c in replace1)
            return replace2

        if opcode in ["LPM"]:
            LPM_OPCODE = {"Z": "1001000ddddd0100", "Z+": "1001000ddddd0101"}

            if len(operands) > 0:
                if int(operands[0][1:]) < 16:
                    raise "Only R16-R31 accessible"
                pattern = LPM_OPCODE[operands[1]]
                destination = f"{int(operands[0][1:]):05b}"
            else:
                return "1001010111001000"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "d" else c for c in pattern)
            return replace1
        
        if opcode in ["SPM"]:
            return self.pattern_list[opcode]

        if opcode in [
            "ADC",
            "ADD",
            "AND",
            "CP",
            "CPC",
            "CPSE",
            "EOR",
            "MOV",
            "MUL",
            "OR",
            "SBC",
            "SUB",
        ]:
            pattern = self.pattern_list[opcode]

            destination = f"{int(operands[0][1:]):05b}"
            source = f"{int(operands[1][1:]):05b}"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "d" else c for c in pattern)
            it = iter(source)
            replace2 = "".join(next(it) if c == "r" else c for c in replace1)

            return replace2

        if opcode in [
            "MULS",
        ]:
            pattern = self.pattern_list[opcode]

            destination = f"{int(operands[0][1:]) - 16:04b}"
            source = f"{int(operands[1][1:]) - 16:04b}"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "d" else c for c in pattern)
            it = iter(source)
            replace2 = "".join(next(it) if c == "r" else c for c in replace1)

            return replace2

        if opcode in [
            "FMUL",
            "FMULS",
            "FMULSU",
        ]:
            pattern = self.pattern_list[opcode]

            destination = f"{int(operands[0][1:]) - 16:03b}"
            source = f"{int(operands[1][1:]) - 16:03b}"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "d" else c for c in pattern)
            it = iter(source)
            replace2 = "".join(next(it) if c == "r" else c for c in replace1)

            return replace2

        if opcode in [
            "ASR",
            "COM",
            "DEC",
            "INC",
            "LSR",
            "NEG",
            "POP",
            "PUSH",
            "ROR",
            "SWAP",
        ]:
            pattern = self.pattern_list[opcode]

            destination = f"{int(operands[0][1:]):05b}"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "d" else c for c in pattern)

            return replace1

        if opcode == "SER":
            pattern = self.pattern_list[opcode]

            destination = f"{int(operands[0][1:]):05b}"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "d" else c for c in pattern)

            return replace1

        if opcode in ["BST", "BLD"]:
            pattern = self.pattern_list[opcode]

            destination = f"{int(operands[0][1:]):05b}"
            bit = f"{int(operands[1]):03b}"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "d" else c for c in pattern)
            it = iter(bit)
            replace2 = "".join(next(it) if c == "b" else c for c in replace1)
            return replace2

        if opcode in ["SBI", "CBI", "SBIC", "SBIS"]:
            pattern = self.pattern_list[opcode]

            destination = f"{int(operands[0], 16):05b}"
            bit = f"{int(operands[1]):03b}"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "A" else c for c in pattern)
            it = iter(bit)
            replace2 = "".join(next(it) if c == "b" else c for c in replace1)
            return replace2

        if opcode in ["BRBC", "BRBS"]:
            pattern = self.pattern_list[opcode]

            offset = self.labels[operands[1]] - (self.PC + 1)
            unsigned = offset & 0x7F

            bit = f"{int(operands[0]):03b}"
            destination = f"{unsigned:07b}"

            it = iter(bit)
            replace1 = "".join(next(it) if c == "s" else c for c in pattern)
            it = iter(destination)
            replace2 = "".join(next(it) if c == "k" else c for c in replace1)
            return replace2
        if opcode in ["BCLR"]:
            pattern = self.pattern_list[opcode]

            bit = f"{int(operands[0]):03b}"

            it = iter(bit)
            replace1 = "".join(next(it) if c == "s" else c for c in pattern)
            return replace1

        if opcode in [
            "BRCC",
            "BRCS",
            "BREQ",
            "BRGE",
            "BRHC",
            "BRHS",
            "BRID",
            "BRIE",
            "BRLO",
            "BRLT",
            "BRMI",
            "BRNE",
            "BRPL",
            "BRSH",
            "BRTC",
            "BRTS",
            "BRVC",
            "BRVS",
        ]:
            pattern = self.pattern_list[opcode]

            offset = self.labels[operands[0]] - (self.PC + 1)
            unsigned = offset & 0x7F

            destination = f"{unsigned:07b}"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "k" else c for c in pattern)
            return replace1

        if opcode in ["BSET"]:
            pattern = self.pattern_list[opcode]

            bit = f"{int(operands[0]):03b}"

            it = iter(bit)
            replace1 = "".join(next(it) if c == "s" else c for c in pattern)
            return replace1

        if opcode in ["RJMP", "RCALL"]:
            pattern = self.pattern_list[opcode]

            offset = (self.labels[operands[0]] - (self.PC + 1)) & 0xFFF

            destination = f"{offset:012b}"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "k" else c for c in pattern)

            return replace1

        if opcode in ["JMP", "CALL"]:
            pattern = self.pattern_list[opcode]

            destination = f"{self.labels[operands[0]]:022b}"
            it = iter(destination)
            replace1 = "".join(next(it) if c == "k" else c for c in pattern)

            return replace1

        if opcode in ["LD", "LDD"]:
            pattern = None
            if operands[1] == "X":
                pattern = "1001000ddddd1100"
            if operands[1] == "X+":
                pattern = "1001000ddddd1101"
            if operands[1] == "-X":
                pattern = "1001000ddddd1110"
            if operands[1] == "Y":
                pattern = "1000000ddddd1000"
            if operands[1] == "Y+":
                pattern = "1001000ddddd1001"
            if operands[1] == "-Y":
                pattern = "1001000ddddd1010"
            if operands[1].startswith("Y+") and opcode == "LDD":
                pattern = "10q0qq0ddddd1qqq"

                destination = f"{int(operands[0][1:]):05b}"
                displacement = f"{int(operands[1][2:]):06b}"

                it = iter(destination)
                replace1 = "".join(next(it) if c == "d" else c for c in pattern)
                it = iter(displacement)
                replace2 = "".join(next(it) if c == "q" else c for c in replace1)
                return replace2
            if operands[1] == "Z":
                pattern = "1000000ddddd0000"
            if operands[1] == "Z+":
                pattern = "1001000ddddd0001"
            if operands[1] == "-Z":
                pattern = "1001000ddddd0010"
            if operands[1].startswith("Z+") and opcode == "LDD":
                pattern = "10q0qq0ddddd0qqq"

                destination = f"{int(operands[0][1:]):05b}"
                displacement = f"{int(operands[1][2:]):06b}"

                it = iter(destination)
                replace1 = "".join(next(it) if c == "d" else c for c in pattern)
                it = iter(displacement)
                replace2 = "".join(next(it) if c == "q" else c for c in replace1)
                return replace2

            destination = f"{int(operands[0][1:]):05b}"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "d" else c for c in pattern)

            return replace1

        if opcode in ["ST", "STD"]:
            pattern = None
            if operands[0] == "X":
                pattern = "1001001rrrrr1100"
            if operands[0] == "X+":
                pattern = "1001001rrrrr1101"
            if operands[0] == "-X":
                pattern = "1001001rrrrr1110"
            if operands[0] == "Y":
                pattern = "1000001rrrrr1000"
            if operands[0] == "Y+":
                pattern = "1001001rrrrr1001"
            if operands[0] == "-Y":
                pattern = "1001001rrrrr1010"
            if operands[0].startswith("Y+") and opcode == "STD":
                pattern = "10q0qq1rrrrr1qqq"

                destination = f"{int(operands[1][1:]):05b}"
                displacement = f"{int(operands[0][2:]):06b}"

                it = iter(destination)
                replace1 = "".join(next(it) if c == "r" else c for c in pattern)
                it = iter(displacement)
                replace2 = "".join(next(it) if c == "q" else c for c in replace1)
                return replace2

            if operands[0] == "Z":
                pattern = "1000001rrrrr0000"
            if operands[0] == "Z+":
                pattern = "1001001rrrrr0001"
            if operands[0] == "-Z":
                pattern = "1001001rrrrr0010"
            if operands[0].startswith("Z+") and opcode == "STD":
                pattern = "10q0qq1rrrrr0qqq"

                destination = f"{int(operands[1][1:]):05b}"
                displacement = f"{int(operands[0][2:]):06b}"

                it = iter(destination)
                replace1 = "".join(next(it) if c == "r" else c for c in pattern)
                it = iter(displacement)
                replace2 = "".join(next(it) if c == "q" else c for c in replace1)
                return replace2

            destination = f"{int(operands[1][1:]):05b}"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "r" else c for c in pattern)

            return replace1

        if opcode in ["LDS", "STS"]:
            pattern = self.pattern_list[opcode]

            if opcode == "LDS":
                destination = f"{int(operands[0][1:]):05b}"
                data = f"{int(operands[1], 16):016b}"

            if opcode == "STS":
                data = f"{int(operands[0], 16):016b}"
                destination = f"{int(operands[1][1:]):05b}"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "d" else c for c in pattern)
            it = iter(data)
            replace2 = "".join(next(it) if c == "k" else c for c in replace1)

            return replace2

        if opcode in ["IN", "OUT"]:
            pattern = self.pattern_list[opcode]

            if opcode == "IN":
                register = f"{int(operands[0][1:]):05b}"
                data = f"{int(operands[1], 16):06b}"
            
                it = iter(data)
                replace1 = "".join(next(it) if c == "A" else c for c in pattern)
                it = iter(register)
                replace2 = "".join(next(it) if c == "d" else c for c in replace1)
                
            elif opcode == "OUT":
                data = f"{int(operands[0], 16):06b}"
                register = f"{int(operands[1][1:]):05b}"
                it = iter(data)
                replace1 = "".join(next(it) if c == "A" else c for c in pattern)
                it = iter(register)
                replace2 = "".join(next(it) if c == "r" else c for c in replace1)
                

            return replace2

        if opcode in [
            "SEC",
            "CLC",
            "SEN",
            "CLN",
            "SEZ",
            "CLZ",
            "SEI",
            "CLI",
            "SES",
            "CLS",
            "SEV",
            "CLV",
            "SET",
            "CLT",
            "SEH",
            "CLH",
        ]:
            return self.pattern_list[opcode]

        if opcode in ["CLR"]:
            pattern = self.pattern_list[opcode]

            destination = f"{int(operands[0][1:]):010b}"

            it = iter(destination)
            replace1 = "".join(next(it) if c == "d" else c for c in pattern)

            return replace1

        if opcode in [
            "NOP",
            "SLEEP",
            "WDR",
            "IJMP",
            "ICALL",
            "RET",
            "RETI",
        ]:
            return self.pattern_list[opcode]

        raise "OPCODE not registered"

    def parser_line(self, line):
        clear = self.clear_line(line)
        if not clear == None:
            symbol = clear[0]

            if symbol.startswith(".org"):
                self.counter = int(clear[1], 16)
                self.PC = int(clear[1], 16)
            elif symbol.startswith(".equ"):
                value = str(clear[1]).replace(" ", "").split("=")
                self.symbols[value[0]] = value[1]
            elif str(symbol).endswith(":"):
                name = symbol.replace(":", "")
                self.labels[name] = self.counter
            elif clear[0] in ["JMP", "CALL", "STS"]:
                self.counter += 1
                return clear
            else:
                return clear
        else:
            return

    def save_to(self, binary):
        with open(self.save_path, "wb") as f:
            for value in binary:
                f.write(struct.pack("<H", value))

    def run(self):
        lines = self.read()

        syntax = []

        for line in lines:
            parser = self.parser_line(line)
            if parser != None:
                syntax.append(line)
                self.counter += 1

        encoded = [0] * 0x4000
        for instruction in syntax:
            result = self.encode(instruction)
            print(f"{self.PC:08X}: {int(result, 2):016b} -> {instruction.strip()}")

            if len(result) > 16:
                part1 = result[:16]
                part2 = result[16:]
                encoded[self.PC] = int(part1, 2)
                encoded[self.PC+1] = int(part2, 2)
                self.PC += 2
            else:
                encoded[self.PC] = int(result, 2)
                self.PC += 1

        self.save_to(encoded)


if __name__ == "__main__":
    assembler = Assembler("./script.asm", "flash.bin")
    result = assembler.run()
