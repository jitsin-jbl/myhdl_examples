

from myhdl import *
from bbbus import BareBoneBus

from stitch_bb_controller import StitchBusController

class SignalPath(object): pass
class MII(object): pass


def stitch_top(
    clock,   # system clock
    reset,   # system reset
    
    # ~~~[Signal IO 0]~~~
    adc0_clk,
    adc0_data,
    adc0_ctrl,
    
    dac0_clk,
    dac0_data,
    dac0_ctrl,

    # ~~~[Signal IO 1]~~~
    adc1_clk,
    adc1_data,
    adc1_ctrl,

    dac1_clk,
    dac1_data,
    dac1_ctrl,

    # ~~~[MII Interface]~~~
    mii_txclk,
    mii_txd,
    mii_txen,
    mii_txer,

    mii_rxclk,
    mii_rxd,
    mii_rxdv,
    mii_rxer,

    mii_col,
    mii_cs
    ):
    """
    """

    # wrap the top-level ports into objects for simplified 
    # interfaces
    sp0 = SignalPath()
    sp0.adc_clk = adc0_clk; sp0.adc_data = adc0_data; sp0.adc_ctrl = adc0_ctrl
    sp0.dac_clk = dac0_clk; sp0.dac_data = dac0_data; sp0.dac_ctrl = dac0_ctrl
    sp1 = SignalPath()
    sp1.adc_clk = adc1_clk; sp1.adc_data = adc1_data; sp1.adc_ctrl = adc1_ctrl
    sp1.dac_clk = dac1_clk; sp1.dac_data = dac1_data; sp1.dac_ctrl = dac1_ctrl

    mii = MII()
    mii.tclk = mii_txclk
    mii.txd = mii_txd
    mii.txen = mii_txen
    mii.txer = mii_txer
    mii.rclk = mii_rxclk
    mii.rxd = mii_rxd
    mii.rxdv = mii_rxdv
    mii.rxer = mii_rxer
    mii.col = mii_col
    mii.cs = mii_cs


    bb = BareBoneBus()
    sbc = StitchBusController()
    bbc = sbc.wrapper(sp0, mii, bb)

    bb_clk, bb_rst = (bb.clk, bb.rst)
    @always_comb
    def hdl_assigns():
        bb_clk.next = clock
        bb_rst.next = reset

    return bbc, hdl_assigns
    

def convert():
    """ Convert the "stitch" example """

    
    clock = Signal(False)
    reset = Signal(False)
    
    adc0_clk = Signal(False)
    adc0_data = Signal(intbv(0)[8:])    
    adc0_ctrl = Signal(intbv(0)[4:])
    
    dac0_clk = Signal(False)
    dac0_data = Signal(intbv(0)[8:])
    dac0_ctrl = Signal(intbv(0)[4:])

    adc1_clk = Signal(False)
    adc1_data = Signal(intbv(0)[8:])
    adc1_ctrl = Signal(intbv(0)[4:])

    dac1_clk = Signal(False)
    dac1_data = Signal(intbv(0)[8:])
    dac1_ctrl = Signal(intbv(0)[4:])

    mii_txclk = Signal(False)    
    mii_txd = Signal(intbv(0)[4:])
    mii_txen = Signal(False)
    mii_txer = Signal(False)

    mii_rxclk = Signal(False)
    mii_rxd = Signal(intbv(0)[4:])
    mii_rxdv = Signal(False)
    mii_rxer = Signal(False)

    mii_col = Signal(False)
    mii_cs =  Signal(False)
 
    toVerilog(stitch_top, clock, reset,
              adc0_clk, adc0_data, adc0_ctrl,
              dac0_clk, dac0_data, dac0_ctrl,
              adc1_clk, adc1_data, adc1_ctrl,
              dac1_clk, dac1_data, dac1_ctrl,
              mii_txclk, mii_txd, mii_txen, mii_txer,
              mii_rxclk, mii_rxd, mii_rxdv, mii_rxer,
              mii_col, mii_cs)


if __name__ == '__main__': convert()
