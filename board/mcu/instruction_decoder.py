class InstructionDecoder:
    def __init__(self, program_memory):
        self.program_memory = program_memory
        self.ALU = None
        
    def set_ALU(self, alu):
        self.ALU = alu

    def signed_12bit(self, value):
        value &= 0xFFF
        return value - 4096 if value > 2047 else value

    def signed_8bit(self, value):
        value &= 0xFF
        return value - 256 if value > 127 else value

    def decode(self, address, code, disassembly=False):
        if code >> 10 & 0b111111 == 0b000111:
            d = code >> 4 & 0b11111
            r = (code >> 9 & 0b1) << 4 | code & 0b1111
            if disassembly:
                return f"ADC R{d}, R{r}"
            else:
                return self.ALU.ADC(d, r)
        elif code >> 10 & 0b111111 == 0b000011:
            d = code >> 4 & 0b11111
            r = (code >> 9 & 0b1) << 4 | code & 0b1111
            if disassembly:
                return f"ADD R{d}, R{r}"
            else:
                self.ALU.ADD(d, r)
        elif code >> 8 & 0b11111111 == 0b10010110:
            d = (code >> 4 & 0b11) + 24
            K = (code >> 6 & 0b11) << 4 | code & 0b1111
            if disassembly:
                return f"ADIW R{d}, {hex(K)}"
            else:
                self.ALU.ADIW(d, K)
        elif code >> 10 & 0b111111 == 0b001000:
            d = code >> 4 & 0b11111
            r = (code >> 9 & 0b1) << 4 | code & 0b1111
            if disassembly:
                return f"AND R{d}, R{r}"
            else:
                self.ALU.AND(d, r)
        elif code >> 12 & 0b1111 == 0b0111:
            d = (code >> 4 & 0b1111) + 16
            K = (code >> 8 & 0b11) << 4 | code & 0b1111
            print(d, K)
            if disassembly:
                return f"ANDI R{d}, {hex(K)}"
            else:
                self.ALU.ANDI(d, K)
        elif code & 0b1111 == 0b0101 and code >> 9 & 0b1111111 == 0b1001010:
            d = code >> 4 & 0b11111
            if disassembly:
                return f"ASR R{d}"
            else:
                self.ALU.ASR(d)
        elif code & 0b1111 == 1000 and code >> 7 & 0b111111111 == 0b100101001:
            s = code >> 4 & 0b111
            if disassembly:
                return f"BCLR {s}"
            else:
                self.ALU.BCLR(s)
        elif code >> 3 & 0b1 == 0 and code >> 9 & 0b1111111 == 0b1111100:
            d = code >> 4 & 0b11111
            b = code & 0b111
            if disassembly:
                return f"BLD R{d}, {b}"
            else:
                self.ALU.BLD(d, b)

        elif code >> 10 & 0b111111 == 0b111101:
            s = code & 0b111
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRBC {s}, {hex(k)}"
            else:
                self.ALU.BRBC(s, k)
        elif code >> 10 & 0b111111 == 0b111100:
            s = code & 0b111
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRBS {s}, {hex(k)}"
            else:
                self.ALU.BRBS(s, k)
        elif code & 0b111 == 0b000 and code >> 10 & 0b111111 == 0b111101:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRCC {hex(k)}"
            else:
                self.ALU.BRCC(k)
        elif code & 0b111 == 0b000 and code >> 10 & 0b111111 == 0b111100:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRCS {hex(k)}"
            else:
                self.ALU.BRCS(k)
        elif code == 0b1001010110011000:
            if disassembly:
                return f"BREAK"

        elif code & 0b111 == 0b001 and code >> 10 & 0b111111 == 0b111100:
            s = code & 0b111
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BREQ {s}, {hex(k)}"
            else:
                self.ALU.BREQ(s, k)
        elif code & 0b111 == 0b100 and code >> 10 & 0b111111 == 0b111101:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRGE {hex(k)}"
            else:
                self.ALU.BRGE(k)
        elif code & 0b111 == 0b101 and code >> 10 & 0b111111 == 0b111101:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRHC {hex(k)}"
            else:
                self.ALU.BRHC(k)
        elif code & 0b111 == 0b101 and code >> 10 & 0b111111 == 0b111100:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRHS {hex(k)}"
            else:
                self.ALU.BRHS(k)
        elif code & 0b111 == 0b111 and code >> 10 & 0b111111 == 0b111101:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRID {hex(k)}"
            else:
                self.ALU.BRID(k)
        elif code & 0b111 == 0b111 and code >> 10 & 0b111111 == 0b111100:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRIE {hex(k)}"
            else:
                self.ALU.BRIE(k)
        elif code & 0b111 == 0b000 and code >> 10 & 0b111111 == 0b111100:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRLO {hex(k)}"
            else:
                self.ALU.BRLO(k)
        elif code & 0b111 == 0b100 and code >> 10 & 0b111111 == 0b111100:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRLT {hex(k)}"
            else:
                self.ALU.BRLT(k)
        elif code & 0b111 == 0b010 and code >> 10 & 0b111111 == 0b111100:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRMI {hex(k)}"
            else:
                self.ALU.BRLO(k)
        elif code & 0b111 == 0b001 and code >> 10 & 0b111111 == 0b111101:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRNE {hex(k)}"
            else:
                self.ALU.BRNE(k)
        elif code & 0b111 == 0b010 and code >> 10 & 0b111111 == 0b111101:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRPL {hex(k)}"
            else:
                self.ALU.BRPL(k)
        elif code & 0b111 == 0b000 and code >> 10 & 0b111111 == 0b111101:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRSH {hex(k)}"
            else:
                self.ALU.BRSH(k)
        elif code & 0b111 == 0b110 and code >> 10 & 0b111111 == 0b111101:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRTC {hex(k)}"
            else:
                self.ALU.BRTC(k)
        elif code & 0b111 == 0b110 and code >> 10 & 0b111111 == 0b111100:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRTS {hex(k)}"
            else:
                self.ALU.BRTS(k)
        elif code & 0b111 == 0b011 and code >> 10 & 0b111111 == 0b111101:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRVC {hex(k)}"
            else:
                self.ALU.BRVC(k)
        elif code & 0b111 == 0b011 and code >> 10 & 0b111111 == 0b111100:
            k = code >> 3 & 0b1111111
            if disassembly:
                return f"BRVS {hex(k)}"
            else:
                self.ALU.BRVS(k)
        elif code & 0b1111 == 0b1000 and code >> 7 & 0b111111111 == 0b100101000:
            s = code >> 4 & 0b111
            if disassembly:
                return f"BSET {s}"
            else:
                self.ALU.BSET(s)
        elif code >> 0b111 & 0b1 == 0 and code >> 9 & 0b1111111 == 0b1111101:
            d = code >> 4 & 0b11111
            b = code & 0b111
            if disassembly:
                return f"BST R{d}, {b}"
            else:
                self.ALU.BST(d, b)
        elif code >> 1 & 0b111 == 0b111 and code >> 9 & 0b1111111 == 0b1001010:
            if disassembly:
                part2 = self.program_memory.memory[address + 1]
            else:
                part2 = self.program_memory.memory[address]

            k = ((code >> 4 & 0b11111) << 1 | code & 0b1) << 16 | part2

            if disassembly:
                return f"CALL {hex(k)}"
            else:
                self.ALU.CALL(k)

        elif code >> 8 & 0b11111111 == 0b10011000:
            A = code >> 3 & 0b11111
            b = code & 0b111
            if disassembly:
                return f"CBI {hex(A)}, {b}"
            else:
                self.ALU.CBI(A, b)
        elif code & 0xFFFF == 0b1001010010001000:
            if disassembly:
                return f"CLC"
            else:
                self.ALU.CLC()
        elif code & 0xFFFF == 0b1001010011011000:
            if disassembly:
                return f"CLH"
            else:
                self.ALU.CLH()
        elif code & 0xFFFF == 0b1001010011111000:
            if disassembly:
                return f"CLI"
            else:
                self.ALU.CLI()
        elif code & 0xFFFF == 0b1001010010101000:
            if disassembly:
                return f"CLC"
            else:
                self.ALU.CLC()
        elif code >> 10 & 0b111111 == 0b001001:
            Rd1 = code & 0b11111
            Rd2 = code & 0b11111
            if disassembly:
                return f"CLR R{Rd1}"
            else:
                self.ALU.CLR(Rd1, Rd2)
        elif code & 0xFFFF == 0b1001010011001000:
            if disassembly:
                return f"CLS"
            else:
                self.ALU.CLS(d, r)
        elif code & 0xFFFF == 0b1001010011101000:
            if disassembly:
                return f"CLT"
            else:
                self.ALU.CLT()
        elif code & 0xFFFF == 0b1001010010111000:
            if disassembly:
                return f"CLV"
            else:
                self.ALU.CLV(d, r)
        elif code & 0xFFFF == 0b1001010010011000:
            if disassembly:
                return f"CLZ"
            else:
                self.ALU.CLZ(d, r)
        elif code >> 9 & 0b1111111 == 0b1001010 and code & 0b1111 == 0000:
            d = code >> 4 & 0b11111
            if disassembly:
                return f"COM R{d}"
            else:
                self.ALU.COM(d)
        elif code >> 10 & 0b111111 == 0b000101:
            d = code >> 4 & 0b11111
            r = (code >> 9 & 0b1) << 4 | code & 0b1111
            if disassembly:
                return f"CP R{d}, R{r}"
            else:
                self.ALU.CP(d, r)
        elif code >> 10 & 0b111111 == 0b000001:
            d = code >> 4 & 0b11111
            r = (code >> 9 & 0b1) << 4 | code & 0b1111
            if disassembly:
                return f"CPC R{d}, R{r}"
            else:
                self.ALU.CPC(d, r)
        elif code >> 12 & 0b1111 == 0b0011:
            d = code >> 4 & 0b11
            K = (code >> 6 & 0b11) << 4 | code & 0b1111
            if disassembly:
                return f"CPI R{d}, {hex(K)}"
            else:
                self.ALU.CPI(d, K)
        elif code >> 10 & 0b111111 == 0b000100:
            d = code >> 4 & 0b11111
            r = (code >> 9 & 0b1) << 4 | code & 0b1111
            if disassembly:
                return f"CPSE R{d}, R{r}"
            else:
                self.ALU.CPSE(d, r)
        elif code & 0b1111 == 0b1010 and code >> 9 & 0b1111111 == 0b1001010:
            d = code >> 4 & 0b11111
            if disassembly:
                return f"DEC R{d}"
            else:
                self.ALU.DEC(d)
        elif code >> 10 & 0b111111 == 0b001001:
            d = code >> 4 & 0b11111
            r = (code >> 9 & 0b1) << 4 | code & 0b1111
            if disassembly:
                return f"EOR R{d}, R{r}"
            else:
                self.ALU.EOR(d, r)
        elif code >> 3 & 0b1 == 0b1 and code >> 7 & 0b111111111 == 0b000000110:
            d = (code >> 4 & 0b111) + 16
            r = (code & 0b111) + 16
            if disassembly:
                return f"FMUL R{d}, R{r}"
            else:
                self.ALU.FMUL(d, r)
        elif code >> 3 & 0b1 == 0b0 and code >> 7 & 0b111111111 == 0b000000111:
            d = (code >> 4 & 0b111) + 16
            r = (code & 0b111) + 16

            if disassembly:
                return f"FMULS"
            else:
                self.ALU.FMULS(d, r)
        elif code >> 3 & 0b1 == 0b1 and code >> 7 & 0b111111111 == 0b000000111:
            d = (code >> 4 & 0b111) + 16
            r = (code & 0b111) + 16
            if disassembly:
                return f"FMULSU"
            else:
                self.ALU.FMULSU(d, r)
        elif code & 0xFFFF == 0b1001010100001001:
            if disassembly:
                return f"ICALL"
            else:
                self.ALU.ICALL()
        elif code & 0xFFFF == 0b1001010000001001:
            if disassembly:
                return f"IJMP"
            else:
                self.ALU.IJMP()
        elif code >> 11 & 0b11111 == 0b10110:
            d = code >> 4 & 0b11111
            A = (code >> 9 & 0b11) << 4 | code & 0b1111
            if disassembly:
                return f"IN R{d}, {hex(A)}"
            else:
                self.ALU.IN(d, A)
        elif code & 0b1111 == 0b0011 and code >> 9 & 0b1111111 == 0b1001010:
            d = code >> 4 & 0b11111
            if disassembly:
                return f"INC R{d}"
            else:
                self.ALU.INC(d)
        elif code >> 1 & 0b111 == 0b110 and code >> 9 & 0b1111111 == 0b1001010:
            if disassembly:
                part2 = self.program_memory.memory[address + 1]
            else:
                part2 = self.program_memory.memory[address]

            k = (code >> 4 & 0b11111) << 1 | code & 0b1 << 16 | part2
            if disassembly:
                return f"JMP {hex(k)}"
            else:
                self.ALU.JMP(k)
        elif (
            code >> 3 & 0b1 == 1
            and code >> 9 & 0b1 == 0
            and code >> 12 & 0b1 == 0
            and code >> 14 & 0b11 == 0b10
        ):
            q = (code >> 13 & 0b1) << 2 | (code >> 12 & 0b11) << 3 | code & 0b111
            d = code >> 4 & 0b11111
            if disassembly:
                return f"LDD R{d}, Y+{q}"
            else:
                self.ALU.LDDY(d, q)
        elif (
            code >> 14 & 0b11 == 0b10
            and code >> 12 & 0b1 == 0
            and code >> 9 & 0b1 == 0
            and code >> 3 & 0b1 == 0
        ):
            q = (code >> 13 & 0b1) << 2 | (code >> 12 & 0b11) << 3 | code & 0b111
            d = code >> 4 & 0b11111
            if disassembly:
                return f"LDD R{d}, Z+{q}"
            else:
                self.ALU.LDDZ(d, q)
        elif (
            code >> 9 & 0b1111111 == 0b1000000
            or code >> 9 & 0b1111111 == 0b1001000
            and code & 0b1111
            in [
                0b1100,
                0b1101,
                0b1110,
                0b1000,
                0b1001,
                0b1010,
                0b0000,
                0b0001,
                0b0010,
            ]
        ):
            symbol = {
                0b1100: "X",
                0b1101: "X+",
                0b1110: "-X",
                0b1000: "Y",
                0b1001: "Y+",
                0b1010: "-Y",
                0b0000: "Z",
                0b0001: "Z+",
                0b0010: "-Z",
            }

            uniq = code & 0b1111
            d = code >> 4 & 0b11111

            if disassembly:
                return f"LD R{d}, {symbol[uniq]}"
            else:
                self.ALU.LD(d, symbol[uniq])

        elif code >> 12 & 0b1111 == 0b1110:
            d = (code >> 4 & 0b1111) + 16
            K = (code >> 8 & 0b1111) << 4 | code & 0b1111
            if disassembly:
                return f"LDI R{d}, {hex(K)}"
            else:
                self.ALU.LDI(d, K)
        elif code & 0b1111 == 0b0000 and code >> 9 & 0b1111111 == 0b1001000:
            d = code >> 4 & 0b11111
            k = self.program_memory.memory[address + 1]
            if disassembly:
                return f"LDS R{d}, {hex(k)}"
            else:
                self.ALU.LDS(d, k)
        elif code & 0xFFFF == 0b1001010111001000:
            if disassembly:
                return f"LPM"
            else:
                self.ALU.LPM(0b0, 0b0)
        elif code & 0b1111 == 0b0100 and code >> 9 & 0b1111111 == 0b1001000:
            d = code >> 4 & 0b11111

            if disassembly:
                return f"LPM R{d}, Z"
            else:
                self.ALU.LPM(d, 0b01)
        elif code & 0b1111 == 0b0101 and code >> 9 & 0b1111111 == 0b1001000:
            d = code >> 4 & 0b11111

            if disassembly:
                return f"LPM R{d}, Z+"
            else:
                self.ALU.LPM(d, 0b10)
        elif code & 0b1111 == 0b0110 and code >> 9 & 0b1111111 == 0b1001010:
            d = code >> 4 & 0b11111
            if disassembly:
                return f"LSR R{d}"
            else:
                self.ALU.LSR(d, r)
        elif code >> 10 & 0b111111 == 0b001011:
            d = code >> 4 & 0b11111
            r = (code >> 9 & 0b1) << 4 | code & 0b1111
            if disassembly:
                return f"MOV R{d}, R{r}"
            else:
                self.ALU.MOV(d, r)
        elif code >> 8 & 0xFF == 0b00000001:
            d = (code >> 4 & 0b1111) * 2
            r = (code & 0b1111) * 2
            if disassembly:
                return f"MOVW R{d+1}:R{d}, R{r+1}:R{r}"
            else:
                self.ALU.MOVW(d, r)
        elif code >> 10 & 0b111111 == 0b100111:
            d = code >> 4 & 0b11111
            r = (code >> 9 & 0b1) << 4 | code & 0b1111
            if disassembly:
                return f"MUL R{d}, R{r}"
            else:
                self.ALU.MUL(d, r)
        elif code >> 8 & 0xFF == 0b00000010:
            d = (code >> 4 & 0b1111) + 16
            r = (code & 0b1111) + 16
            if disassembly:
                return f"MULS R{d}, R{r}"
            else:
                self.ALU.MULS(d, r)
        elif code >> 3 & 0b1 == 0b0 and code >> 7 & 0b111111111 == 0b000000110:
            d = (code >> 4 & 0b111) + 16
            r = (code & 0b111) + 16

            if disassembly:
                return f"MULSU R{d}, R{r}"
            else:
                self.ALU.MULSU(d, r)
        elif code & 0b1111 == 0b0001 and code >> 9 & 0b1111111 == 0b1001010:
            d = code >> 4 & 0b11111
            if disassembly:
                return f"NEG R{d}"
            else:
                self.ALU.NEG(d)
        elif code & 0xFFFF == 0b0000000000000000:
            if disassembly:
                return f"NOP"
        elif code >> 10 & 0b111111 == 0b001010:
            d = code >> 4 & 0b11111
            r = (code >> 9 & 0b1) << 4 | code & 0b1111
            if disassembly:
                return f"OR R{d}, R{r}"
            else:
                self.ALU.OR(d, r)
        elif code >> 12 & 0b1111 == 0b0110:
            d = code >> 4 & 0b11
            K = (code >> 6 & 0b11) << 4 | code & 0b1111
            if disassembly:
                return f"ORI R{d}, {hex(K)}"
            else:
                self.ALU.ORI(d, K)
        elif code >> 11 & 0b11111 == 0b10111:
            r = code >> 4 & 0b11111
            A = (code >> 9 & 0b11) << 4 | code & 0b1111
            if disassembly:
                return f"OUT {hex(A)}, R{r}"
            else:
                self.ALU.OUT(A, r)
        elif code & 0b1111 == 0b1111 and code >> 9 & 0b1111111 == 0b1001000:
            r = code >> 4 & 0b11111
            if disassembly:
                return f"POP R{r}"
            else:
                self.ALU.POP(r)
        elif code & 0b1111 == 0b1111 and code >> 9 & 0b1111111 == 0b1001001:
            r = code >> 4 & 0b11111
            if disassembly:
                return f"PUSH R{r}"
            else:
                self.ALU.PUSH(r)
        elif code >> 12 & 0b1111 == 0b1101:
            k = self.signed_12bit(code)
            if disassembly:
                return f"RCALL {hex(k)}"
            else:
                self.ALU.RCALL(k)
        elif code & 0xFFFF == 0b1001010100001000:
            if disassembly:
                return f"RET"
            else:
                self.ALU.RET()
        elif code & 0xFFFF == 0b1001010100011000:
            if disassembly:
                return f"RETI"
            else:
                self.ALU.RETI()
        elif code >> 12 & 0b1111 == 0b1100:
            k = self.signed_12bit((code & 0xFFF))
            if disassembly:
                return f"RJMP {hex(k)}"
            else:
                self.ALU.RJMP(k)

        elif code >> 10 & 0b111111 == 0b000111:
            d = code & 0b11111
            r = code >> 5 & 0b11111
            # BELUM
            if disassembly:
                return f"ROL R{d}, R{r}"
            else:
                self.ALU.ROL(d)
        elif code & 0b1111 == 0b0111 and code >> 9 & 0b1111111 == 0b1001010:
            d = code >> 4 & 0b11111
            if disassembly:
                return f"ROR R{d}"
            else:
                self.ALU.ROR(d)
        elif code >> 10 & 0b111111 == 0b000010:
            d = code >> 4 & 0b11111
            r = (code >> 9 & 0b1) << 4 | code & 0b1111
            if disassembly:
                return f"SBC R{d}, R{r}"
            else:
                self.ALU.SBC(d, r)
        elif code >> 12 & 0b1111 == 0b0100:
            d = code >> 4 & 0b11
            K = (code >> 6 & 0b11) << 4 | code & 0b1111
            if disassembly:
                return f"SBCI R{d}, {hex(K)}"
            else:
                self.ALU.SBCI(d, K)
        elif code >> 8 & 0xFF == 0b10011010:
            A = code >> 3 & 0b11111
            b = code & 0b111
            if disassembly:
                return f"SBI {hex(A)}, {b}"
            else:
                self.ALU.SBI(A, b)
        elif code >> 8 & 0xFF == 0b10011001:
            A = code >> 3 & 0b11111
            b = code & 0b111
            if disassembly:
                return f"SBIC {hex(A)}, {b}"
            else:
                self.ALU.SBIC(A, b)
        elif code >> 8 & 0xFF == 0b10011011:
            A = code >> 3 & 0b11111
            b = code & 0b111
            if disassembly:
                return f"SBIS {hex(A)}, {b}"
            else:
                self.ALU.SBIS(A, b)
        elif code >> 8 & 0xFF == 0b10010111:
            d = code >> 4 & 0b11
            K = (code >> 6 & 0b11) << 4 | code & 0b1111
            if disassembly:
                return f"SBIW"
            else:
                self.ALU.SBIW(d, r)
        elif code >> 12 & 0b1111 == 0b0110:
            d = code >> 4 & 0b11
            K = (code >> 6 & 0b11) << 4 | code & 0b1111
            if disassembly:
                return f"SBR R{d}, {hex(K)}"
            else:
                self.ALU.SBR(d, K)
        elif code >> 3 & 0b1 == 0b0 and code >> 9 & 0b1111111 == 0b1111110:
            r = code >> 4 & 0b11111
            b = code & 0b111
            if disassembly:
                return f"SBRC"
            else:
                self.ALU.SBRC(d, r)
        elif code >> 3 & 0b1 == 0b0 and code >> 9 & 0b1111111 == 0b1111111:
            r = code >> 4 & 0b11111
            b = code & 0b111
            if disassembly:
                return f"SBRS R{r}, {b}"
            else:
                self.ALU.SBRS(r, b)
        elif code & 0xFFFF == 0b1001010000001000:
            if disassembly:
                return f"SEC"
            else:
                self.ALU.SEC()
        elif code & 0xFFFF == 0b1001010001011000:
            if disassembly:
                return f"SEH"
            else:
                self.ALU.SEH()
        elif code & 0xFFFF == 0b1001010001111000:
            if disassembly:
                return f"SEI"
            else:
                self.ALU.SEI()
        elif code & 0xFFFF == 0b1001010000101000:
            if disassembly:
                return f"SEN"
            else:
                self.ALU.SEN()
        elif code & 0b1111 == 0b1111 and code >> 8 & 0b11111111 == 0b11101111:
            d = code >> 4 & 0b1111
            if disassembly:
                return f"SER R{d}"
            else:
                self.ALU.SER()
        elif code & 0xFFFF == 0b1001010001001000:
            if disassembly:
                return f"SES"
            else:
                self.ALU.SES()
        elif code & 0xFFFF == 0b1001010001101000:
            if disassembly:
                return f"SET"
            else:
                self.ALU.SET()
        elif code & 0xFFFF == 0b1001010000111000:
            if disassembly:
                return f"SEV"
            else:
                self.ALU.SEV()
        elif code & 0xFFFF == 0b1001010000011000:
            if disassembly:
                return f"SEZ"
            else:
                self.ALU.SEZ()
        elif code & 0xFFFF == 0b1001010110001000:
            if disassembly:
                return f"SLEEP"
            else:
                self.ALU.SLEEP()
        elif code & 0xFFFF == 0b1001010111101000:
            if disassembly:
                return f"SPM"
            else:
                self.ALU.SPM()
        elif (
            code >> 14 & 0b11 == 0b10
            and code >> 12 & 0b1 == 0
            and code >> 9 & 0b1 == 1
            and code >> 3 & 0b1 == 1
        ):
            q = (code >> 13 & 0b1) << 2 | (code >> 12 & 0b11) << 3 | code & 0b111
            r = code >> 4 & 0b11111
            if disassembly:
                return f"STD R{r}, Y+{q}"
            else:
                self.ALU.STDY(r, q)
        elif (
            code >> 14 & 0b11 == 0b10
            and code >> 12 & 0b1 == 0
            and code >> 9 & 0b1 == 1
            and code >> 3 & 0b1 == 0
        ):
            q = (code >> 13 & 0b1) << 2 | (code >> 12 & 0b11) << 3 | code & 0b111
            r = code >> 4 & 0b11111
            if disassembly:
                return f"STD R{r}, Z+{q}"
            else:
                self.ALU.STDZ(r, q)
        elif (
            code >> 9 & 0b1111111 == 0b1001001
            or code >> 9 & 0b1111111 == 0b1000001
            and code & 0b1111
            in [
                0b1100,
                0b1101,
                0b1110,
                0b1000,
                0b1001,
                0b1010,
                0b0000,
                0b0001,
                0b0010,
            ]
        ):
            symbol = {
                0b1100: "X",
                0b1101: "X+",
                0b1110: "-X",
                0b1000: "Y",
                0b1001: "Y+",
                0b1010: "-Y",
                0b0000: "Z",
                0b0001: "Z+",
                0b0010: "-Z",
            }

            uniq = code & 0b1111
            r = code >> 4 & 0b11111

            if disassembly:
                return f"ST R{r}, {symbol[uniq]}"
            else:
                self.ALU.ST(r, symbol[uniq])

        elif code & 0b1111 == 0b0000 and code >> 9 & 0b1111111 == 0b1001001:
            d = code >> 4 & 0b11111

            if disassembly:
                k = self.program_memory.memory[address + 1]
            else:
                k = self.program_memory.memory[address]

            if disassembly:
                return f"STS {hex(k)}, R{d}"
            else:
                self.ALU.STS(k, d)
        elif code >> 10 & 0b111111 == 0b000110:
            d = code >> 4 & 0b11111
            r = (code >> 9 & 0b1) << 4 | code & 0b1111
            if disassembly:
                return f"SUB R{d}, R{r}"
            else:
                self.ALU.SUB(d, r)
        elif code >> 12 & 0b1111 == 0b0101:
            d = code >> 4 & 0b11
            K = (code >> 6 & 0b11) << 4 | code & 0b1111
            if disassembly:
                return f"SUBI R{d}, {hex(K)}"
            else:
                self.ALU.SUBI(d, K)
        elif code & 0b1111 == 0b0010 and code >> 9 & 0b1111111 == 0b1001010:
            d = code >> 4 & 0b11111
            if disassembly:
                return f"SWAP R{d}"
            else:
                self.ALU.SWAP(d)
        elif code >> 10 & 0b111111 == 0b001000:
            d = code & 0b11111
            if disassembly:
                return f"TST"
            else:
                self.ALU.TST(d)
        elif code & 0xFFFF == 0b1001010110101000:
            if disassembly:
                return f"WDR"
            else:
                self.ALU.WDR(d, r)
        else:
            if disassembly:
                return f"{hex(code)} Unknown Opcode"
        # CBR
