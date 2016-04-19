
from myhdl import *

def TOP(clk,out1,out2):
    rom = tuple([ii for ii in range(10)])
    @always(clk.posedge)
    def rom_logic():
        out1.next=rom[3]
        out2.next=rom[9]
    return rom_logic

if __name__ == '__main__':
    out1 = Signal(intbv(0)[8:])
    out2 = Signal(intbv(0)[8:])
    clk = Signal(False)
toVHDL(TOP, clk, out1, out2)
