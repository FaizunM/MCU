class ALU:
    def __init__(self, PC, program_memory, data_memory, bls):
        self.PC = PC
        self.program_memory = program_memory
        self.data_memory = data_memory
        self.bls = bls

    # Arithmetic and Logic Instructions SECTION
    def ADD(self, Rd, Rs):
        a = self.data_memory.get_GPR(Rd)
        b = self.data_memory.get_GPR(Rs)

        r = a + b

        H = 1 if ((a & 0x0F) + (b & 0x0F)) > 0x0F else 0
        self.data_memory.set_SREG_bit("H", H)
        V = ((~(a ^ b) & (a ^ r)) >> 7) & 1
        self.data_memory.set_SREG_bit("V", V)
        N = (r >> 7) & 1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if r == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if (a + b) > 0xFF else 0
        self.data_memory.set_SREG_bit("C", C)

        self.data_memory.set_GPR(Rd, r)

    def ADC(self, Rd, Rr):
        a = self.data_memory.get_GPR(Rd)
        b = self.data_memory.get_GPR(Rr)
        c_in = self.data_memory.get_SREG_bit("C")

        r = a + b + c_in

        H = 1 if ((a & 0x0F) + (b & 0x0F) + c_in) > 0x0F else 0
        self.data_memory.set_SREG_bit("H", H)
        V = ((~(a ^ b) & (a ^ r)) >> 7) & 1
        self.data_memory.set_SREG_bit("V", V)
        N = (r >> 7) & 1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if r == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if (a + b + c_in) > 0xFF else 0
        self.data_memory.set_SREG_bit("C", C)

        self.data_memory.set_GPR(Rd, r)

    def ADIW(self, Rd, K):
        high = self.data_memory.get_GPR(Rd + 1) & 0xFF
        low = self.data_memory.get_GPR(Rd) & 0xFF

        HL = high << 8 | low

        result = HL + K
        rh = result >> 8 & 0xFF
        rl = result & 0xFF

        V = 1 if ((HL & 0x8000) == 0 and (result & 0x8000) != 0) else 0
        self.data_memory.set_SREG_bit("V", V)
        N = (result >> 15) & 1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if result == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if (HL + K) > 0xFFFF else 0
        self.data_memory.set_SREG_bit("C", C)

        self.data_memory.set_GPR(Rd + 1, rh)
        self.data_memory.set_GPR(Rd, rl)

    def SUB(self, Rd, Rr):
        d = self.data_memory.get_GPR(Rd) & 0xFF
        r = self.data_memory.get_GPR(Rr) & 0xFF

        result = (d - r) & 0xFF

        self.data_memory.set_GPR(Rd, r)

        d7 = (d >> 7) & 1
        r7 = (r >> 7) & 1
        rr7 = (result >> 7) & 1

        H = 1 if (((~d & r) | (r & result) | (result & ~d)) & 0x08) else 0
        self.data_memory.set_SREG_bit("H", H)
        V = 1 if (d7 and not r7 and not rr7) or (not d7 and r7 and rr7) else 0
        self.data_memory.set_SREG_bit("V", V)
        N = rr7
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if (result == 0) else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if (r > d) else 0
        self.data_memory.set_SREG_bit("C", C)

    def SUBI(self, Rd, K):
        d = self.data_memory.get_GPR(Rd) & 0xFF
        r = K & 0xFF

        result = (d - r) & 0xFF

        self.data_memory.set_GPR(Rd, r)

        d7 = (d >> 7) & 1
        r7 = (r >> 7) & 1
        rr7 = (result >> 7) & 1

        H = 1 if (((~d & r) | (r & result) | (result & ~d)) & 0x08) else 0
        self.data_memory.set_SREG_bit("H", H)
        V = 1 if (d7 and not r7 and not rr7) or (not d7 and r7 and rr7) else 0
        self.data_memory.set_SREG_bit("V", V)
        N = rr7
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if (result == 0) else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if (r > d) else 0
        self.data_memory.set_SREG_bit("C", C)

    def SBC(self, Rd, Rr):
        d = self.data_memory.get_GPR(Rd) & 0xFF
        r = self.data_memory.get_GPR(Rr) & 0xFF
        c_in = self.data_memory.get_SREG_bit("C") & 1

        result = (d - r - c_in) & 0xFF

        self.data_memory.set_GPR(Rd, r)

        d7 = (d >> 7) & 1
        r7 = (r >> 7) & 1
        rr7 = (result >> 7) & 1

        H = 1 if (((~d & r) | (r & result) | (result & ~d)) & 0x08) else 0
        self.data_memory.set_SREG_bit("H", H)
        V = 1 if (d7 and not r7 and not rr7) or (not d7 and r7 and rr7) else 0
        self.data_memory.set_SREG_bit("V", V)
        N = rr7
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if (result == 0) else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if ((r + c_in) > d) else 0
        self.data_memory.set_SREG_bit("C", C)

    def SBCI(self, Rd, K):
        d = self.data_memory.get_GPR(Rd) & 0xFF
        r = K & 0xFF
        c_in = self.data_memory.get_SREG_bit("C") & 1

        result = (d - r - c_in) & 0xFF

        self.data_memory.set_GPR(Rd, r)

        d7 = (d >> 7) & 1
        r7 = (r >> 7) & 1
        rr7 = (result >> 7) & 1

        H = 1 if (((~d & r) | (r & result) | (result & ~d)) & 0x08) else 0
        self.data_memory.set_SREG_bit("H", H)
        V = 1 if (d7 and not r7 and not rr7) or (not d7 and r7 and rr7) else 0
        self.data_memory.set_SREG_bit("V", V)
        N = rr7
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if (result == 0) else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if ((r + c_in) > d) else 0
        self.data_memory.set_SREG_bit("C", C)

    def SBIW(self, Rd, K):
        d1 = self.data_memory.get_GPR(Rd + 1) & 0xFF
        d2 = self.data_memory.get_GPR(Rd) & 0xFF

        d = d1 << 8 | d2 & 0xFFFF
        r = K & 0xFF

        result = (d - r) & 0xFFFF

        result1 = result >> 8 & 0xFF
        result2 = result & 0xFF

        self.data_memory.set_GPR(Rd + 1, result1)
        self.data_memory.set_GPR(Rd, result2)

        V = 1 if ((d >> 15 == 0) and ((result >> 15) == 1)) else 0
        self.data_memory.set_SREG_bit("V", V)
        N = (result >> 15) & 1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if (result == 0) else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if (r > d) else 0
        self.data_memory.set_SREG_bit("C", C)

    def AND(self, Rd, Rr):
        a = self.data_memory.get_GPR(Rd)
        b = self.data_memory.get_GPR(Rr)

        r = a & b

        V = 0
        self.data_memory.set_SREG_bit("V", V)
        N = (r >> 7) & 1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if r == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)

        self.data_memory.set_GPR(Rd, r)

    def ANDI(self, Rd, K):
        a = self.data_memory.get_GPR(Rd)

        r = a & K

        V = 0
        self.data_memory.set_SREG_bit("V", V)
        N = (r >> 7) & 1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if r == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)

        self.data_memory.set_GPR(Rd, r)

    def OR(self, Rd, Rr):
        a = self.data_memory.get_GPR(Rd)
        b = self.data_memory.get_GPR(Rr)

        r = a | b

        V = 0
        self.data_memory.set_SREG_bit("V", V)
        N = (r >> 7) & 1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if r == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)

        self.data_memory.set_GPR(Rd, r)

    def ORI(self, Rd, K):
        a = self.data_memory.get_GPR(Rd) & 0xFF
        b = K & 0xFF

        r = a | b

        V = 0
        self.data_memory.set_SREG_bit("V", V)
        N = (r >> 7) & 1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if r == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)

        self.data_memory.set_GPR(Rd, r)

    def EOR(self, Rd, Rr):
        a = self.data_memory.get_GPR(Rd)
        b = self.data_memory.get_GPR(Rr)

        r = a ^ b

        V = 0
        self.data_memory.set_SREG_bit("V", V)
        N = (r >> 7) & 1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if r == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)

        self.data_memory.set_GPR(Rd, r)

    def COM(self, Rd):
        d = self.data_memory.get_GPR(Rd) & 0xFF

        r = 0xFF - d

        self.data_memory.set_GPR(Rd, r)

        V = 0
        self.data_memory.set_SREG_bit("V", V)
        N = r >> 7 & 0b1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if r == 0x0 else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1
        self.data_memory.set_SREG_bit("C", C)

    def NEG(self, Rd):
        d = self.data_memory.get_GPR(Rd) & 0xFF

        R = (-d) & 0xFF

        self.data_memory.set_GPR(Rd, R)

        H = 1 if (d & 0x0F) != 0 else 0
        self.data_memory.set_SREG_bit("H", H)
        V = 1 if d == 0x80 else 0
        self.data_memory.set_SREG_bit("V", V)
        N = (R >> 7) & 0b1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if R == 0x0 else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if d != 0 else 0
        self.data_memory.set_SREG_bit("C", C)

    def SBR(self, Rd, K):
        a = self.data_memory.get_GPR(Rd) & 0xFF
        b = K & 0xFF

        r = a | b

        V = 0
        self.data_memory.set_SREG_bit("V", V)
        N = (r >> 7) & 1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if r == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)

        self.data_memory.set_GPR(Rd, r)

    def CBR(self, Rd, K):
        a = self.data_memory.get_GPR(Rd) & 0xFF
        b = (0xFF - K) & 0xFF

        r = a | b

        V = 0
        self.data_memory.set_SREG_bit("V", V)
        N = (r >> 7) & 1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if r == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)

        self.data_memory.set_GPR(Rd, r)

    def INC(self, Rd):
        d = self.data_memory.get_GPR(Rd) & 0xFF

        R = d + 1

        self.data_memory.set_GPR(Rd, R)

        V = 1 if R == 0x7F else 0
        self.data_memory.set_SREG_bit("V", V)
        N = (R >> 7) & 1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if (R == 0) else 0
        self.data_memory.set_SREG_bit("Z", Z)

    def DEC(self, Rd):
        d = self.data_memory.get_GPR(Rd) & 0xFF

        R = d - 1

        self.data_memory.set_GPR(Rd, R)

        V = 1 if R == 0x7F else 0
        self.data_memory.set_SREG_bit("V", V)
        N = (R >> 7) & 1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if (R == 0) else 0
        self.data_memory.set_SREG_bit("Z", Z)

    def TST(self, Rd):
        a = self.data_memory.get_GPR(Rd)

        r = (a & a) & 0xFF

        V = 0
        self.data_memory.set_SREG_bit("V", V)
        N = (r >> 7) & 1
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if r == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)

        self.data_memory.set_GPR(Rd, r)

    def CLR(self, Rd1, Rd2):
        a = self.data_memory.get_GPR(Rd1) & 0xFF
        b = self.data_memory.get_GPR(Rd2) & 0xFF

        result = a ^ b

        self.data_memory.set_GPR(Rd1, result)

        self.data_memory.set_SREG_bit("S", 0)
        self.data_memory.set_SREG_bit("V", 0)
        self.data_memory.set_SREG_bit("N", 0)
        self.data_memory.set_SREG_bit("Z", 1)

    def SER(self, Rd):
        self.data_memory.set_GPR(Rd, 0xFF)

    def MUL(self, Rd, Rr):
        a = self.data_memory.get_GPR(Rd) & 0xFF
        b = self.data_memory.get_GPR(Rr) & 0xFF

        R = a * b

        self.data_memory.set_GPR(Rd + 1, R >> 8 & 0xFF)
        self.data_memory.set_GPR(Rd, R & 0xFF)

        Z = 1 if R == 0x0 else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if R >> 15 & 1 else 0
        self.data_memory.set_SREG_bit("C", C)

    def signed_12bit(self, value):
        value &= 0xFFF
        return value - 4096 if value > 2047 else value

    def signed_8bit(self, value):
        value &= 0xFF
        return value - 256 if value > 127 else value

    def MULS(self, Rd, Rr):
        a = self.signed_8bit(self.data_memory.get_GPR(Rd))
        b = self.signed_8bit(self.data_memory.get_GPR(Rr))

        R = a * b

        self.data_memory.set_GPR(Rd + 1, R >> 8 & 0xFF)
        self.data_memory.set_GPR(Rd, R & 0xFF)

        Z = 1 if R == 0x0 else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if R >> 15 & 1 else 0
        self.data_memory.set_SREG_bit("C", C)

    def MULSU(self, Rd, Rr):
        a = self.signed_8bit(self.data_memory.get_GPR(Rd))
        b = self.data_memory.get_GPR(Rr)

        R = a * b

        self.data_memory.set_GPR(Rd + 1, R >> 8 & 0xFF)
        self.data_memory.set_GPR(Rd, R & 0xFF)

        Z = 1 if R == 0x0 else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if R >> 15 & 1 else 0
        self.data_memory.set_SREG_bit("C", C)

    def FMUL(self, Rd, Rr):
        a = self.data_memory.get_GPR(Rd) & 0xFF
        b = self.data_memory.get_GPR(Rr) & 0xFF

        temp = a * b
        R = temp << 1

        self.data_memory.set_GPR(Rd + 1, (R >> 8) & 0xFF)
        self.data_memory.set_GPR(Rd, R & 0xFF)

        Z = 1 if R == 0xFFFF else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if R >> 0xFFFF else 0
        self.data_memory.set_SREG_bit("C", C)

    def FMULS(self, Rd, Rr):
        a = self.signed_8bit(self.data_memory.get_GPR(Rd)) & 0xFF
        b = self.signed_8bit(self.data_memory.get_GPR(Rr)) & 0xFF

        temp = a * b
        R = temp << 1

        self.data_memory.set_GPR(Rd + 1, (R >> 8) & 0xFF)
        self.data_memory.set_GPR(Rd, R & 0xFF)

        Z = 1 if R == 0xFFFF else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if R >> 0xFFFF else 0
        self.data_memory.set_SREG_bit("C", C)

    def FMULSU(self, Rd, Rr):
        a = self.signed_8bit(self.data_memory.get_GPR(Rd)) & 0xFF
        b = self.data_memory.get_GPR(Rr)

        temp = a * b
        R = temp << 1

        self.data_memory.set_GPR(Rd + 1, (R >> 8) & 0xFF)
        self.data_memory.set_GPR(Rd, R & 0xFF)

        Z = 1 if R == 0xFFFF else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if R >> 0xFFFF else 0
        self.data_memory.set_SREG_bit("C", C)

    # Branch Instructions SECTION
    def RJMP(self, k):
        self.PC.counter += k

    def IJMP(self):
        a = self.data_memory.get_GPR(31) & 0xFF
        b = self.data_memory.get_GPR(30) & 0xFF

        k = (a << 8) | b

        self.PC.counter = k

    def JMP(self, k):
        self.PC.counter = k

    def ICALL(self):
        a = self.data_memory.get_GPR(31) & 0xFF
        b = self.data_memory.get_GPR(30) & 0xFF

        k = (a << 8) | b

        next_k = self.PC.counter

        self.data_memory.set_GPIO(0x3E, next_k >> 8 & 0xFF)
        self.data_memory.set_GPIO(0x3D, next_k & 0xFF)

        self.data_memory.StackPointer -= 2

        self.PC.counter += k

    def RCALL(self, k):
        next_k = self.PC.counter

        self.data_memory.set_GPIO(0x3E, next_k >> 8 & 0xFF)
        self.data_memory.set_GPIO(0x3D, next_k & 0xFF)

        self.data_memory.StackPointer -= 2

        self.PC.counter += k

    def CALL(self, k):
        next_k = self.PC.counter + 1

        self.data_memory.set_GPIO(0x3E, next_k >> 8 & 0xFF)
        self.data_memory.set_GPIO(0x3D, next_k & 0xFF)

        self.data_memory.StackPointer -= 2

        self.PC.counter = k

    def RET(self):
        SPH = self.data_memory.get_GPIO(0x3E)
        SPL = self.data_memory.get_GPIO(0x3D)

        SP = SPH << 8 | SPL
        self.data_memory.StackPointer += 2

        self.PC.counter = SP

    def RETI(self):
        SPH = self.data_memory.get_GPIO(0x3E)
        SPL = self.data_memory.get_GPIO(0x3D)

        SP = SPH << 8 | SPL
        self.data_memory.StackPointer += 2

        self.PC.counter = SP

        self.data_memory.set_SREG_bit("I", 1)

    def CPSE(self, Rd, Rr):
        d = self.data_memory.get_GPR(Rd) & 0xFF
        r = self.data_memory.get_GPR(Rr) & 0xFF

        if d == r:
            self.PC.counter += 1

    def CP(self, Rd, Rr):
        d = self.data_memory.get_GPR(Rd) & 0xFF
        r = self.data_memory.get_GPR(Rr) & 0xFF

        result = (d - r) & 0xFF

        d7 = (d >> 7) & 1
        r7 = (r >> 7) & 1
        rr7 = (result >> 7) & 1

        H = 1 if (((~d & r) | (r & result) | (result & ~d)) & 0x08) else 0
        self.data_memory.set_SREG_bit("H", H)
        V = 1 if (d7 and not r7 and not rr7) or (not d7 and r7 and rr7) else 0
        self.data_memory.set_SREG_bit("V", V)
        N = rr7
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if (result == 0) else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if (r > d) else 0
        self.data_memory.set_SREG_bit("C", C)

    def CPC(self, Rd, Rr):
        d = self.data_memory.get_GPR(Rd) & 0xFF
        r = self.data_memory.get_GPR(Rr) & 0xFF
        c_in = self.data_memory.get_SREG_bit("C") & 1

        result = (d - r - c_in) & 0xFF

        d7 = (d >> 7) & 1
        r7 = (r >> 7) & 1
        rr7 = (result >> 7) & 1

        H = 1 if (((~d & r) | (r & result) | (result & ~d)) & 0x08) else 0
        self.data_memory.set_SREG_bit("H", H)
        V = 1 if (d7 and not r7 and not rr7) or (not d7 and r7 and rr7) else 0
        self.data_memory.set_SREG_bit("V", V)
        N = rr7
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if (result == 0) else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if ((r + c_in) > d) else 0
        self.data_memory.set_SREG_bit("C", C)

    def CPI(self, Rd, K):
        d = self.data_memory.get_GPR(Rd) & 0xFF
        r = K & 0xFF

        result = (d - r) & 0xFF

        d7 = (d >> 7) & 1
        r7 = (r >> 7) & 1
        rr7 = (result >> 7) & 1

        H = 1 if (((~d & r) | (r & result) | (result & ~d)) & 0x08) else 0
        self.data_memory.set_SREG_bit("H", H)
        V = 1 if (d7 and not r7 and not rr7) or (not d7 and r7 and rr7) else 0
        self.data_memory.set_SREG_bit("V", V)
        N = rr7
        self.data_memory.set_SREG_bit("N", N)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if (result == 0) else 0
        self.data_memory.set_SREG_bit("Z", Z)
        C = 1 if (r > d) else 0
        self.data_memory.set_SREG_bit("C", C)

    def SBRC(self, Rr, b):
        r = self.data_memory.get_GPR(Rr) & 0xFF

        if (r >> b & 0b1) == 0:
            self.PC.counter += 1

    def SBRS(self, Rr, b):
        r = self.data_memory.get_GPR(Rr) & 0xFF

        if (r >> b & 0b1) == 1:
            self.PC.counter += 1

    def SBIC(self, A, b):
        r = self.data_memory.get_GPIO(A) & 0xFF

        b = r >> b & 0b1
        if b == 0:
            self.PC.counter += 1

    def SBIS(self, A, b):
        r = self.data_memory.get_GPIO(A) & 0xFF

        b = r >> b & 0b1
        if b == 1:
            self.PC.counter += 1

    def BRBS(self, s, k):
        a = self.data_memory.get_SREG_bit(self.data_memory.flags[s])

        if a == 1:
            self.PC.counter += k

    def BRBC(self, s, k):
        a = self.data_memory.get_SREG_bit(self.data_memory.flags[s])

        if a == 0:
            self.PC.counter += k

    def BREQ(self, k):
        a = self.data_memory.get_SREG_bit("Z")

        if a == 1:
            self.PC.counter += k

    def BRNE(self, k):
        a = self.data_memory.get_SREG_bit("Z")

        if a == 0:
            self.PC.counter += k

    def BRCS(self, k):
        a = self.data_memory.get_SREG_bit("C")

        if a == 1:
            self.PC.counter += k

    def BRCC(self, k):
        a = self.data_memory.get_SREG_bit("C")

        if a == 0:
            self.PC.counter += k

    def BRSH(self, k):
        a = self.data_memory.get_SREG_bit("C")

        if a == 0:
            self.PC.counter += k

    def BRLO(self, k):
        a = self.data_memory.get_SREG_bit("C")

        if a == 1:
            self.PC.counter += k

    def BRMI(self, k):
        a = self.data_memory.get_SREG_bit("N")

        if a == 1:
            self.PC.counter += k

    def BRPL(self, k):
        a = self.data_memory.get_SREG_bit("N")

        if a == 0:
            self.PC.counter += k

    def BRGE(self, k):
        a = self.data_memory.get_SREG_bit("S")

        if a == 0:
            self.PC.counter += k

    def BRLT(self, k):
        a = self.data_memory.get_SREG_bit("S")

        if a == 1:
            self.PC.counter += k

    def BRHS(self, k):
        a = self.data_memory.get_SREG_bit("H")

        if a == 1:
            self.PC.counter += k

    def BRHC(self, k):
        a = self.data_memory.get_SREG_bit("H")

        if a == 0:
            self.PC.counter += k

    def BRTS(self, k):
        a = self.data_memory.get_SREG_bit("T")

        if a == 1:
            self.PC.counter += k

    def BRTC(self, k):
        a = self.data_memory.get_SREG_bit("T")

        if a == 0:
            self.PC.counter += k

    def BRVS(self, k):
        a = self.data_memory.get_SREG_bit("V")

        if a == 1:
            self.PC.counter += k

    def BRVC(self, k):
        a = self.data_memory.get_SREG_bit("V")

        if a == 0:
            self.PC.counter += k

    def BRIE(self, k):
        a = self.data_memory.get_SREG_bit("I")

        if a == 1:
            self.PC.counter += k

    def BRID(self, k):
        a = self.data_memory.get_SREG_bit("I")

        if a == 0:
            self.PC.counter += k

    # Bit and Bit-Test Instructions SECTION
    def SBI(self, A, b):
        a = self.data_memory.get_GPIO(A)

        mask = 1 << b

        R = a ^ mask
        self.data_memory.set_GPIO(A, R)

    def CBI(self, A, b):
        a = self.data_memory.get_GPIO(A)

        mask = ~(1 << b)

        R = a ^ mask
        self.data_memory.set_GPIO(A, R)

    def LSL(self, Rd):
        d = self.data_memory.get_GPR(Rd) & 0xFF

        d7 = d >> 7 & 1

        R = (d << 1) & 0xFF

        H = d >> 3 & 1
        self.data_memory.set_SREG_bit("C", H)
        C = d7
        self.data_memory.set_SREG_bit("C", C)
        Z = 1 if R == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)
        N = (R >> 7) & 1
        self.data_memory.set_SREG_bit("N", N)
        V = N ^ C
        self.data_memory.set_SREG_bit("V", V)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)

    def LSR(self, Rd):
        d = self.data_memory.get_GPR(Rd) & 0xFF

        d0 = d & 0b1

        R = (d >> 1) & 0xFF

        C = d0
        self.data_memory.set_SREG_bit("C", C)
        Z = 1 if R == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)
        N = 0
        self.data_memory.set_SREG_bit("N", N)
        V = N ^ C
        self.data_memory.set_SREG_bit("V", V)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)

    def ROL(self, Rd):
        d = self.data_memory.get_GPR(Rd) & 0xFF
        c_old = self.data_memory.get_SREG_bit("C")

        d7 = d >> 7 & 1

        R = ((d << 1) | c_old) & 0xFF

        H = d >> 3 & 1
        self.data_memory.set_SREG_bit("C", H)
        C = d7
        self.data_memory.set_SREG_bit("C", C)
        Z = 1 if R == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)
        N = (R >> 7) & 1
        self.data_memory.set_SREG_bit("N", N)
        V = N ^ C
        self.data_memory.set_SREG_bit("V", V)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)

    def ROR(self, Rd):
        d = self.data_memory.get_GPR(Rd) & 0xFF
        c_old = self.data_memory.get_SREG_bit("C")

        d0 = d & 0b1

        R = ((d >> 1) | c_old) & 0xFF

        C = d0
        self.data_memory.set_SREG_bit("C", C)
        Z = 1 if R == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)
        N = R >> 7 & 1
        self.data_memory.set_SREG_bit("N", N)
        V = N ^ C
        self.data_memory.set_SREG_bit("V", V)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)

    def ASR(self, Rd):
        a = self.data_memory.get_GPR(Rd)

        r = a >> 1

        self.data_memory.set_GPR(Rd, r)

        C = a & 0b1
        self.data_memory.set_SREG_bit("C", C)
        N = (r >> 7) & 1
        self.data_memory.set_SREG_bit("N", N)
        V = N ^ C
        self.data_memory.set_SREG_bit("V", V)
        S = N ^ V
        self.data_memory.set_SREG_bit("S", S)
        Z = 1 if r == 0 else 0
        self.data_memory.set_SREG_bit("Z", Z)

    def SWAP(self, Rd):
        d = self.data_memory.get_GPR(Rd) & 0xFF

        HN = d >> 4 & 0b1111
        LN = d & 0b1111

        R = LN << 4 | HN

        self.data_memory.set_GPR(Rd, R)

    def BSET(self, s):
        self.data_memory.set_SREG_bit(self.data_memory.flags[s], 1)

    def BCLR(self, s):
        self.data_memory.set_SREG_bit(self.data_memory.flags[s], 0)

    def BST(self, Rd, b):
        a = self.data_memory.get_GPR(Rd)

        r = a >> b & 0b1

        self.data_memory.set_SREG_bit("T", r)

    def BLD(self, Rd, b):
        a = self.data_memory.get_GPR(Rd)
        bit = self.data_memory.get_SREG_bit("T")

        mask = 1 << b
        if bit == 1:
            a |= mask
        else:
            a &= mask

        self.data_memory.set_GPR(Rd & 0xFF, a)

    def SEC(self):
        self.data_memory.set_SREG_bit("C", 1)

    def CLC(self):
        self.data_memory.set_SREG_bit("C", 0)

    def SEN(self):
        self.data_memory.set_SREG_bit("N", 1)

    def CLN(self):
        self.data_memory.set_SREG_bit("N", 0)

    def SEZ(self):
        self.data_memory.set_SREG_bit("Z", 1)

    def CLZ(self):
        self.data_memory.set_SREG_bit("Z", 0)

    def SEI(self):
        self.data_memory.set_SREG_bit("I", 1)

    def CLI(self):
        self.data_memory.set_SREG_bit("I", 0)

    def SES(self):
        self.data_memory.set_SREG_bit("S", 1)

    def CLS(self):
        self.data_memory.set_SREG_bit("S", 0)

    def SEV(self):
        self.data_memory.set_SREG_bit("V", 1)

    def CLV(self):
        self.data_memory.set_SREG_bit("V", 0)

    def SET(self):
        self.data_memory.set_SREG_bit("T", 1)

    def CLT(self):
        self.data_memory.set_SREG_bit("T", 0)

    def SEH(self):
        self.data_memory.set_SREG_bit("H", 1)

    def CLH(self):
        self.data_memory.set_SREG_bit("H", 0)

    # Data Transfer Instructions SECTION
    def MOV(self, Rd, Rr):
        r = self.data_memory.get_GPR(Rr) & 0xFF

        self.data_memory.set_GPR(Rd, r)

    def MOVW(self, Rd, Rr):
        ra = self.data_memory.get_GPR(Rr + 1) & 0xFF
        rb = self.data_memory.get_GPR(Rr) & 0xFF

        self.data_memory.set_GPR(Rd + 1, ra)
        self.data_memory.set_GPR(Rd, rb)

    def LDI(self, Rd, K):
        self.data_memory.set_GPR(Rd, K)

    def LD(self, Rd, XYZ):
        if XYZ == "X":
            AH = self.data_memory.get_GPR(27) & 0xFF
            AL = self.data_memory.get_GPR(26) & 0xFF

            A = AH << 8 | AL
            R = self.data_memory.get(A)
            self.data_memory.set_GPR(Rd, R)
        if XYZ == "X+":
            AH = self.data_memory.get_GPR(27) & 0xFF
            AL = self.data_memory.get_GPR(26) & 0xFF

            A = AH << 8 | AL
            R = self.data_memory.get(A)
            self.data_memory.set_GPR(Rd, R)

            A += 1
            self.data_memory.set_GPR(27, A >> 8 & 0xFF)
            self.data_memory.set_GPR(26, A & 0xFF)
        if XYZ == "-X":
            AH = self.data_memory.get_GPR(27) & 0xFF
            AL = self.data_memory.get_GPR(26) & 0xFF

            A = AH << 8 | AL
            R = self.data_memory.get(A)
            self.data_memory.set_GPR(Rd, R)

            A -= 1
            self.data_memory.set_GPR(27, A >> 8 & 0xFF)
            self.data_memory.set_GPR(26, A & 0xFF)

        if XYZ == "Y":
            AH = self.data_memory.get_GPR(29) & 0xFF
            AL = self.data_memory.get_GPR(28) & 0xFF

            A = AH << 8 | AL
            R = self.data_memory.get(A)
            self.data_memory.set_GPR(Rd, R)
        if XYZ == "Y+":
            AH = self.data_memory.get_GPR(29) & 0xFF
            AL = self.data_memory.get_GPR(28) & 0xFF

            A = AH << 8 | AL
            R = self.data_memory.get(A)
            self.data_memory.set_GPR(Rd, R)

            A += 1
            self.data_memory.set_GPR(29, A >> 8 & 0xFF)
            self.data_memory.set_GPR(28, A & 0xFF)
        if XYZ == "-Y":
            AH = self.data_memory.get_GPR(29) & 0xFF
            AL = self.data_memory.get_GPR(28) & 0xFF

            A = AH << 8 | AL
            R = self.data_memory.get(A)
            self.data_memory.set_GPR(Rd, R)

            A -= 1
            self.data_memory.set_GPR(29, A >> 8 & 0xFF)
            self.data_memory.set_GPR(28, A & 0xFF)

        if XYZ == "Z":
            AH = self.data_memory.get_GPR(31) & 0xFF
            AL = self.data_memory.get_GPR(30) & 0xFF

            A = AH << 8 | AL
            R = self.data_memory.get(A)
            self.data_memory.set_GPR(Rd, R)
        if XYZ == "Z+":
            AH = self.data_memory.get_GPR(31) & 0xFF
            AL = self.data_memory.get_GPR(30) & 0xFF

            A = AH << 8 | AL
            R = self.data_memory.get(A)
            self.data_memory.set_GPR(Rd, R)

            A += 1
            self.data_memory.set_GPR(31, A >> 8 & 0xFF)
            self.data_memory.set_GPR(30, A & 0xFF)
        if XYZ == "-Z":
            AH = self.data_memory.get_GPR(31) & 0xFF
            AL = self.data_memory.get_GPR(30) & 0xFF

            A = AH << 8 | AL
            R = self.data_memory.get(A)
            self.data_memory.set_GPR(Rd, R)

            A -= 1
            self.data_memory.set_GPR(31, A >> 8 & 0xFF)
            self.data_memory.set_GPR(30, A & 0xFF)

    def LDDY(self, Rd, q):
        AH = self.data_memory.get_GPR(29) & 0xFF
        AL = self.data_memory.get_GPR(28) & 0xFF

        A = (AH << 8 | AL) + q
        R = self.data_memory.get(A)
        self.data_memory.set_GPR(Rd, R)

    def LDDZ(self, Rd, q):
        AH = self.data_memory.get_GPR(31) & 0xFF
        AL = self.data_memory.get_GPR(30) & 0xFF

        A = (AH << 8 | AL) + q
        R = self.data_memory.get(A)
        self.data_memory.set_GPR(Rd, R)

    def ST(self, Rr, XYZ):
        d = self.data_memory.get_GPR(Rr) & 0xFF
        if XYZ == "X":
            AH = self.data_memory.get_GPR(27) & 0xFF
            AL = self.data_memory.get_GPR(26) & 0xFF

            A = AH << 8 | AL
            self.data_memory.set(A, d)
        if XYZ == "X+":
            AH = self.data_memory.get_GPR(27) & 0xFF
            AL = self.data_memory.get_GPR(26) & 0xFF

            A = AH << 8 | AL
            self.data_memory.set(A, d)

            A += 1
            self.data_memory.set_GPR(27, A >> 8 & 0xFF)
            self.data_memory.set_GPR(26, A & 0xFF)
        if XYZ == "-X":
            AH = self.data_memory.get_GPR(27) & 0xFF
            AL = self.data_memory.get_GPR(26) & 0xFF

            A = AH << 8 | AL
            self.data_memory.set(A, d)

            A -= 1
            self.data_memory.set_GPR(27, A >> 8 & 0xFF)
            self.data_memory.set_GPR(26, A & 0xFF)

        if XYZ == "Y":
            AH = self.data_memory.get_GPR(29) & 0xFF
            AL = self.data_memory.get_GPR(28) & 0xFF

            A = AH << 8 | AL
            self.data_memory.set(A, d)
        if XYZ == "Y+":
            AH = self.data_memory.get_GPR(29) & 0xFF
            AL = self.data_memory.get_GPR(28) & 0xFF

            A = AH << 8 | AL
            self.data_memory.set(A, d)

            A += 1
            self.data_memory.set_GPR(29, A >> 8 & 0xFF)
            self.data_memory.set_GPR(28, A & 0xFF)
        if XYZ == "-Y":
            AH = self.data_memory.get_GPR(29) & 0xFF
            AL = self.data_memory.get_GPR(28) & 0xFF

            A = AH << 8 | AL
            self.data_memory.set(A, d)

            A -= 1
            self.data_memory.set_GPR(29, A >> 8 & 0xFF)
            self.data_memory.set_GPR(28, A & 0xFF)

        if XYZ == "Z":
            AH = self.data_memory.get_GPR(31) & 0xFF
            AL = self.data_memory.get_GPR(30) & 0xFF

            A = AH << 8 | AL
            self.data_memory.set(A, d)
        if XYZ == "Z+":
            AH = self.data_memory.get_GPR(31) & 0xFF
            AL = self.data_memory.get_GPR(30) & 0xFF

            A = AH << 8 | AL
            self.data_memory.set(A, d)

            A += 1
            self.data_memory.set_GPR(31, A >> 8 & 0xFF)
            self.data_memory.set_GPR(30, A & 0xFF)
        if XYZ == "-Z":
            AH = self.data_memory.get_GPR(31) & 0xFF
            AL = self.data_memory.get_GPR(30) & 0xFF

            A = AH << 8 | AL
            self.data_memory.set(A, d)

            A -= 1
            self.data_memory.set_GPR(31, A >> 8 & 0xFF)
            self.data_memory.set_GPR(30, A & 0xFF)

    def STDY(self, Rr, q):
        d = self.data_memory.get_GPR(Rr) & 0xFF

        AH = self.data_memory.get_GPR(29) & 0xFF
        AL = self.data_memory.get_GPR(28) & 0xFF

        A = (AH << 8 | AL) + q
        R = self.data_memory.set(A, d)

    def STDZ(self, Rr, q):
        d = self.data_memory.get_GPR(Rr) & 0xFF

        AH = self.data_memory.get_GPR(31) & 0xFF
        AL = self.data_memory.get_GPR(30) & 0xFF

        A = (AH << 8 | AL) + q
        self.data_memory.set(A, d)

    def STS(self, k, Rd):
        d = self.data_memory.get_GPR(Rd) & 0xFF

        self.data_memory.set(k, d)

    def LPM(self, Rd, Z_type):
        if Rd == 0b0:
            ZH = self.data_memory.get_GPR(31) & 0xFF
            ZL = self.data_memory.get_GPR(30) & 0xFF

            Z = ZH << 8 | ZL
            
        if Z_type == 0b01:
            ZH = self.data_memory.get_GPR(31) & 0xFF
            ZL = self.data_memory.get_GPR(30) & 0xFF

            Z = ZH << 8 | ZL

        if Z_type == 0b10:
            ZH = self.data_memory.get_GPR(31) & 0xFF
            ZL = self.data_memory.get_GPR(30) & 0xFF

            Z = (ZH << 8 | ZL) + 1
        
        byte = self.program_memory.get_data_bus(Z)
        
        if self.bls.lock_bits.BLB0_mode() == 3:
            if (
                self.PC >= self.program_memory.bootloader_start
                and self.PC <= self.program_memory.bootloader_end
            ):
                return
            
        if self.bls.lock_bits.BLB1_mode() == 3:
            if (
                self.PC >= self.program_memory.application_start
                and self.PC <= self.program_memory.application_end
            ):
                return
            
        
        self.data_memory.set_GPR(Rd, byte)

    def SPM(self):
        ZH = self.data_memory.get_GPR(31) & 0xFF
        ZL = self.data_memory.get_GPR(30) & 0xFF

        Z = ZH << 8 | ZL

        if self.bls.lock_bits.BLB0_mode() in [2, 4]:
            if (
                Z >= self.program_memory.bootloader_start
                and Z <= self.program_memory.bootloader_end
            ):
                return
            
        if self.bls.lock_bits.BLB0_mode() == 3:
            if (
                self.PC >= self.program_memory.bootloader_start
                and self.PC <= self.program_memory.bootloader_end
            ):
                return
            
        if self.bls.lock_bits.BLB1_mode() in [2, 4]:
            if (
                Z >= self.program_memory.application_start
                and Z <= self.program_memory.application_end
            ):
                return
        
        if self.bls.lock_bits.BLB1_mode() == 3:
            if (
                self.PC >= self.program_memory.application_start
                and self.PC <= self.program_memory.application_end
            ):
                return
            
        DH = self.data_memory.get_GPR(1) & 0xFF
        DL = self.data_memory.get_GPR(0) & 0xFF

        data = DH << 8 | DL
        self.program_memory.set(Z, data)

    def IN(self, Rd, A):
        data = self.data_memory.get_GPIO(A)

        self.data_memory.set_GPR(Rd, data)

    def OUT(self, A, Rr):
        data = self.data_memory.get_GPR(Rr)

        self.data_memory.set_GPIO(A, data)

    def PUSH(self, Rr):
        data = self.data_memory.get_GPR(Rr)

        self.data_memory.StackPointer -= 1
        address = self.data_memory.StackPointer
        self.data_memory.set(address, data)

    def POP(self, Rd):
        address = self.data_memory.StackPointer
        data = self.data_memory.get(address)

        self.data_memory.set_GPR(Rd, data)

        self.data_memory.StackPointer += 1
