
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

    CLKDV_OUT.driven = "wire"
    CLKIN_IBUFG_OUT.driven = "wire"
    CLK0_OUT.driven = "wire"
    CLKFX_OUT.driven = "wire"
    LOCKED_OUT.driven = "wire"

    return hdl_clkfx, hdl_clk0, hdl_clkdv, hdl_touch_inputs

dcm12MHz.verilog_instance = "ICLK"

def OFDDRCPE(Q, C0, C1, CE, CLR, D0, D1, PRE):
    """
    Note: The body of this module doesn't actually do anything.  
          Just some statements to use the input and outputs
    """
    k = Signal(False)
    @always(C0.posedge, PRE.posedge) 
    def hdl_1():
        if PRE == True:
            k.next = 1
        else:
            k.next = D0 & D1

    @always(C1.posedge, CLR.posedge)
    def hdl_2():
        if CLR == True:
            Q.next = False
        else:
            if CE:
                Q.next = D0 | D1 | k

    
    Q.driven = "wire"

    return hdl_1, hdl_2

OFDDRCPE.verilog_instance = "DDR_CLK"
        

def convert():
    clock = Signal(False)
    reset = Signal(True)
    clk12MHz = Signal(False)
    _clock = Signal(False)
    clk48MHz = Signal(False)
    clk96MHz = Signal(False)
    dcm_locked = Signal(False)

    toVerilog(dcm12MHz, clock, reset, clk12MHz, _clock, 
              clk48MHz, clk96MHz, dcm_locked)

if __name__ == '__main__':
    convert()
    
