
from random import randint
from myhdl import *


def ram(clk, we, din, dout, addr, MemSize=2048):

    mem = [Signal(intbv(0)[8:]) for ii in range(MemSize)]

    @always(clk.posedge)
    def hdl_ram_wr():
        if we:
            mem[addr].next = din

    @always(clk.posedge)
    def hdl_ram_rd():
        dout.next = mem[addr]

    return hdl_ram_wr, hdl_ram_rd


def rom_async(dout, addr, MemSize=1024):

    rom = [randint(0, dout.max-1) for ii in range(MemSize)]
    rom = tuple(rom)

    @always_comb
    def hdl_rom():
        dout.next = rom[addr]

    return hdl_rom


def rom_sync(clk, dout, addr, MemSize=1024):
    
    rom = [randint(0, dout.max-1) for ii in range(MemSize)]
    rom = tuple(rom)

    @always(clk.posedge)
    def hdl_rom():
        dout.next = rom[addr]

    return hdl_rom

def top_ram_rom(clk, we, din, dout):

    dout_ram  = Signal(intbv(0)[8:])
    dout_rom1 = Signal(intbv(0)[8:])
    dout_rom2 = Signal(intbv(0)[8:])
    addr = Signal(intbv(0)[16:])

    @always(clk.posedge)
    def hdl_addr_cnt():
        addr.next = addr + 1

    iRam = ram(clk, we, din, dout_ram, addr)
    iRom1 = rom_async(dout_rom1, addr)
    iRom2 = rom_sync(clk, dout_rom2, addr)

    @always_comb
    def hdl_out():
        dout.next = dout_ram | dout_rom1 | dout_rom2;

    return hdl_addr_cnt, hdl_out, iRam, iRom1, iRom2

def convert():
    clk = Signal(False)
    we = Signal(False)
    din = Signal(intbv(0)[8:])
    dout = Signal(intbv(0)[8:])

    toVerilog(top_ram_rom, clk, we, din, dout)
    toVHDL(top_ram_rom, clk, we, din, dout)

if __name__ == '__main__':
    convert()
