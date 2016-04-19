
import os

from myhdl import *
from myhdl_tools import Clock
from myhdl_tools.boards import get_board
import myhdl_tools as tlz

def m_fpga_inits_top(clock, we, leds, select_rom, 
                     ram_size=2048, rom_size=2048):
    """
    this is an FPGA example with initial value support.  The "mem"
    list of signals should be synthesized as an internal memory.
    When initial value support is enabled the memory should be
    pre-filled.  This should be testable on an FPGA platform with
    a button and LEDs.
    """
    modval = int(2**len(leds))
    cmax = int(clock.frequency)
    ccnt = Signal(intbv(0, min=0, max=cmax))
    mcnt = Signal(modbv(0, min=0, max=ram_size))

    # RAM with initial values
    mem = [Signal(intbv((ii%modval), min=0, max=leds.max)) 
           for ii in range(ram_size)]

    # ROM
    rom = tuple([ii % (modval/2) for ii in range(rom_size)])

    @always(clock.posedge)
    def rtl_cnt():
        if ccnt == 0:
            mcnt.next = mcnt + 1
            
        if ccnt < cmax-1:
            ccnt.next = ccnt + 1
        else:
            ccnt.next = 0

    @always(clock.posedge)
    def rtl_out():
        # write new values to the RAM
        if not we:
            mem[mcnt].next = ccnt%modval
         
        # use the ROM or RAM contents
        if select_rom:
            leds.next = rom[mcnt]
        else:
            leds.next = mem[mcnt]

    return rtl_cnt, rtl_out


def test():
    clock = Clock(0, frequency=10)
    we = Signal(bool(0))
    leds = Signal(intbv(0)[8:])
    srom = Signal(bool(0))

    tbdut = m_fpga_inits_top(clock, we, leds, srom)
    tbclk = clock.gen()

    def _test():
        @instance
        def tbstim():
            for ii in range(3):
                while leds != 127:
                    yield clock.posedge

            # use the ROM values
            srom.next = True

            for ii in range(3):
                while leds != 63:
                    yield clock.posedge

        
            raise StopSimulation
        
        return tbdut, tbclk, tbstim

    if os.path.isfile('_test.vcd'):
        os.remove('_test.vcd')
    Simulation(traceSignals(_test)).run()

    # convert the files
    clock.frequency = 50e6
    toVerilog(m_fpga_inits_top, clock, we, leds, srom)
    toVHDL(m_fpga_inits_top, clock, we, leds, srom)

    # run the design through the FPGA tools
    brd = get_board('atlys', top=m_fpga_inits_top)
    brd.add_port('we', we, pins=('T15',))
    brd.name_port('leds', 'led') # rename the "leds" port to "led" pin
    brd.add_port('select_rom', srom, pins=('N4',))
    brd.run()

if __name__ == '__main__':
    test()
    