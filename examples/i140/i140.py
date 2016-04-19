
from myhdl import *
from myhdl_tools.boards import get_xilinx_board

def m_top(clock,led,btn):
    @always(clock.posedge)
    def rtl():
        led.next = btn
    return rtl

brd = get_xilinx_board('xula')
brd.set_top(m_top)
brd.add_port('btn', Signal(bool(0)), pins=(33,))
brd.add_port('led', Signal(bool(0)), pins=(32,))
brd.run()
