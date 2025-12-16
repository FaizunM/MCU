.org 0x0000
.equ RAMEND = 0x08FF

RJMP Start
NOP

Start:
    LDI R16, 0x14
    LDI R17, 0x15
    CALL TEST
    NOP

TEST:
    PUSH R16
    LDI R16, 0x18
    POP R16
    RET


