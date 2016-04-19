#
#

from myhdl import *
from aic23_spi import *
from aic23_config import Aic23Config

def aic23_setup(
    clock,
    reset,
    pgm,
    aic23_bus,
    # Configuration Parameters
    ConfigOpt
    ):
    """ Static setup / configuration for the AIC23 CODEC

    This module will generate the correct register settings based
    on the configure in ConfigOpt.  This module will drive the
    AIC23 configuration bus (
    """
    
    config_rom,config_addr = ConfigOpt.BuildRom()

    # Local aliases
    AUDIO_CSN = aic23_bus.csn
    AUDIO_SCLK = aic23_bus.sclk
    AUDIO_SDIN = aic23_bus.sdin

    # State types
    States = enum('IDLE', 'RGO', 'BDLY', 'WAIT', 'INC', 'END')
    state  = Signal(States.IDLE)

    aic_c      = Signal(intbv(0)[16:])  # control data
    aic_c_go   = Signal(False)          # send control data
    aic_c_busy = Signal(False)          # sending data
    
    _go        = Signal(False)
    reg_cnt    = Signal(intbv(0)[4:])

    _pgm       = Signal(False)
    pgm_trans  = Signal(False)
    pgm_rst    = Signal(False)

    @always_seq(clock.posedge, reset=reset)
    def hdl_pgm():
        # There appears to be an issue with the @always_seq and the 
        # the following kind of statement.  Need to submit a test that
        # exposes the issue?
        #_pgm.next = pgm        
        if pgm and not _pgm or not pgm_rst:
            pgm_trans.next = True
        else:
            pgm_trans.next = False
        _pgm.next = pgm        

    
    @always_seq(clock.posedge, reset=reset)
    def hdl_sm():
        if state == States.IDLE:
            if pgm_trans:
                state.next = States.RGO
            reg_cnt.next = 0
                
        elif state == States.RGO:
            if not aic_c_busy:
                state.next = States.BDLY
                aic_c_go.next = True

        elif state == States.BDLY:
            aic_c_go.next = False
            state.next = States.WAIT

        elif state == States.WAIT:
            aic_c_go.next = False
            if not aic_c_busy:
                if reg_cnt == 9:
                    state.next = States.END
                else:
                    state.next = States.INC

        elif state == States.INC:
            aic_c_go.next = False
            state.next = States.RGO
            reg_cnt.next = reg_cnt + 1

        elif state == States.END:
            pgm_rst.next  = True   # at least one pgm has been completed
            aic_c_go.next = False
            if pgm_trans:
                state.next = States.IDLE
            else:
                state.next = States.END  

        else:
            assert False, "Unhandled state %s" % (state)
            aic_c_go.next = False
            state.next = States.END

    @always(clock.posedge)
    def hdl_rom_addr_val():
        aic_c.next[9:0] = config_rom[reg_cnt]
        aic_c.next[16:9] = config_addr[reg_cnt]

    SPI = aic23_spi(clock, reset, aic_c, aic_c_go, aic_c_busy,
                    AUDIO_CSN, AUDIO_SCLK, AUDIO_SDIN)


    return instances()
