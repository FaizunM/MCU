.org 0x0000
.equ RAMEND = 0x08FF

RJMP Start

Start:
    LDI R16, 0x20
    LDI R17, 0x00
    OUT 0x05, R16
    OUT 0x04, R17
    NOP