

from myhdl import *

from aic23_setup import *
from aic23_i2s import *

def aic23(
    # --[System Signals]--
    clock,     # also known as fclk
    reset,     # system reset        
    au_bus,    # audio stream   
    aic23_bus, # external codec interface
    tst_pts,   # Output:   test points

    # --[ Parameters ]--
    ConfigOpt = None
    ):
    """AIC23 interface
    This module contains the logic to configure the AIC23 in a default mode
    and transfer audio to and fro.  This module will configure the AIC23 
    """

    # @todo: Read in the configuration file, from the configuration file 
    # generate the correct register configuration.
    if ConfigOpt is None or not isinstance(ConfigOpt, Aic23Config):
        if not isinstance(ConfigOpt, Aic23Config):
            print("WARNING: Invalid AIC23 config type %s, results might not be as expected" % (type(ConfigOpt)))
        ConfigOpt = Aic23Config()

    i2s_tst_pts = Signal(intbv(0)[5:])
        
    # Static Signal
    spi_mode = Signal(True) if aic23_bus.mode else Signal(False)

    AUDIO_CSN = aic23_bus.csn
    AUDIO_SCLK = aic23_bus.sclk
    AUDIO_SDIN = aic23_bus.sdin
    @always(clock.posedge) 
    def hdl_test_points():
        tst_pts.next[5:] = i2s_tst_pts
        tst_pts.next[5]  = AUDIO_CSN
        tst_pts.next[6]  = AUDIO_SCLK
        tst_pts.next[7]  = AUDIO_SDIN

    pgm = Signal(False)
    g_setup = aic23_setup(clock, reset, pgm, aic23_bus,
                          ConfigOpt=ConfigOpt)    
    g_i2s  = aic23_i2s(clock, reset, aic23_bus, au_bus, i2s_tst_pts, 
                       ConfigOpt=ConfigOpt)

        
    
    return hdl_test_points, g_setup, g_i2s


    


    

