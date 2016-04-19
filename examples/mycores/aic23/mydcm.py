
from myhdl import *

# wrapper around a dcm file

def dcm12MHz(CLKIN_IN, RST_IN, CLKDV_OUT, CLKIN_IBUFG_OUT,
             CLK0_OUT, CLKFX_OUT, LOCKED_OUT):

    @always(delay(2))
    def hdl_clkfx():
        CLKFX_OUT.next = not CLKFX_OUT
    
    @always(delay(4))
    def hdl_clk0():
        CLK0_OUT.next = not CLK0_OUT
        CLKIN_IBUFG_OUT.next = not CLKIN_IBUFG_OUT

    @always(delay(16))
    def hdl_clkdv():
        CLKDV_OUT.next = not CLKDV_OUT

    @always_comb
    def hdl_touch_inputs():
        LOCKED_OUT.next = True | CLKIN_IN | RST_IN;

    return hdl_clkfx, hdl_clk0, hdl_clkdv, hdl_touch_inputs

mydcm.verilog_instance = "mydcm"
#mydcm.verilog_code = \
#"""
#dcm12MHz iclk (
#   .CLKIN_IN(${CLKIN_IN}), 
#   .RST_IN(${RST_IN}),             
#   .CLKDV_OUT(${CLKDV_OUT}), 
#   .CLKIN_IBUFG_OUT(${CLKIN_IBUFG_OUT}), 
#   .CLK0_OUT(${CLK0_OUT}), 
#   .CLKFX_OUT(${CLKFX_OUT}),
#   .LOCKED_OUT(${LOCKED_OUT})
#);
#"""


def convert():
    clock = Signal(False)
    reset = ResetSignal(True, active=0, async=True)
    clk12MHz = Signal(False)
    _clock = Signal(False)
    clk48MHz = Signal(False)
    clk96MHz = Signal(False)
    dcm_locked = Signal(False)

    toVerilog(mydcm, clock, reset, clk12MHz, _clock, 
              clk48MHz, clk96MHz, dcm_locked)

if __name__ == '__main__':
    convert()
    
