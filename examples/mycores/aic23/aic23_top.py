
from argparse import Namespace
from myhdl import *
from aic23 import aic23
from aic23_config import Aic23Config
from xip import dcm12MHz, OFDDRCPE

# Pin out for different FPGA boards with AIC23
# [Comment]-------------------------+
# [FPGA Pin]-------------------+    |
# [AIC23 Pin]--------------+   |    |
# [Port Dir]-------+       |   |    |
# [Signal Name]    |       |   |    |
#                  |       |   |    |
# DSPtronics USB FPGA board|   |    |
#------------------+-------+---+----+---------------------------
#AUDIO_CLK,        Output: 25  63   This is driven by top-level DCM->DDR flop 
#AUDIO_BCLK,       Input:  3   85   I2S Serial-bit clock
#AUDIO_DIN,        Output: 4   62   I2S data out of CODEC
#AUDIO_DOUT,       Input:  6   66   I2S data in to CODEC
#AUDIO_LRCIN,      Input:  5   65   I2S DAC-word clock signal
#AUDIO_LRCOUT,     Input:  7   68   I2S ADC-word clock signal
#AUDIO_MODE,       Output: 22  69   0 - 2 wire, 1 - SPI
#AUDIO_CSN,        Output: 21  84   Control Mode chip select
#AUDIO_SCLK,       Output: 24  78   Control port serial clock
#AUDIO_SDIN,       Output: 23  79   Control port serial data
#                  |       |   |    |
# Altera Cyclone II/III DSP board   |
#------------------+-------+---+----+---------------------------
#AUDIO_CLK,        Output: 25  AB3  This is driven by top-level DCM->DDR flop 
#AUDIO_BCLK,       Input:  3   F3   I2S Serial-bit clock
#AUDIO_DIN,        Output: 4   J21  I2S data out of CODEC
#AUDIO_DOUT,       Input:  6   B13  I2S data in to CODEC
#AUDIO_LRCIN,      Input:  5   W4   I2S DAC-word clock signal
#AUDIO_LRCOUT,     Input:  7   AB2  I2S ADC-word clock signal
#AUDIO_MODE,       Output: 22  AA2  0 - 2 wire, 1 - SPI
#AUDIO_CSN,        Output: 21  AC25 Control Mode chip select
#AUDIO_SCLK,       Output: 24  R4   Control port serial clock
#AUDIO_SDIN,       Output: 23  AD2  Control port serial data

class Container(object) : pass

def aic23_top(
    # --[System Signals]--
    clock_in,  # also known as fclk
    reset_in,  # system reset
            
    # --[ External CODEC interface to AIC23, see pinout above comments ]--
    AUDIO_CLK,      # Output:   This is driven by top-level DCM->DDR flop 
    AUDIO_BCLK,      # Input:    I2S Serial-bit clock
    AUDIO_DIN,       # Output:   I2S data out of CODEC
    AUDIO_DOUT,      # Input:    I2S data in to CODEC
    AUDIO_LRCIN,     # Input:    I2S DAC-word clock signal
    AUDIO_LRCOUT,    # Input:    I2S ADC-word clock signal
    AUDIO_MODE,      # Output:   0 - 2 wire, 1 - SPI
    AUDIO_CSN,       # Output:   Control Mode chip select
    AUDIO_SCLK,      # Output:   Control port serial clock
    AUDIO_SDIN,      # Output:   Control port serial data
    tst_pts,         # Output:   test points
    LEDS,            # Input:    7 leds
    # --[ Parameters ]--
    ConfigOpt = None
    ):
    """AIC23 interface
    This module contains the logic to configure the AIC23 in a default mode
    and transfer audio to and fro.
    """

    reset = ResetSignal(True, active=0, async=True)
    iwl = ConfigOpt.input_len
    au_in_r  = Signal(intbv(0)[iwl:]) # audio in stream to FPGA logic right channel
    au_in_l  = Signal(intbv(0)[iwl:]) # audio in stream to FPGA logic left channel 
    au_out_r = Signal(intbv(0)[iwl:]) # audio out stream from FPGA logic right channel
    au_out_l = Signal(intbv(0)[iwl:]) # audio out stream from FPGA logic left channel
    mic_in   = Signal(intbv(0)[iwl:]) # Mic audio stream
    hp_out   = Signal(intbv(0)[iwl:]) # Speaker audio stream
    Ts       = Signal(False)          # Sample rate pulse

    # The external bus to the AIC23 CODEC
    aic23_bus = Namespace(bclk=AUDIO_BCLK, din=AUDIO_DIN, dout=AUDIO_DOUT,
                          lrcin=AUDIO_LRCIN, lrcout=AUDIO_LRCOUT, mode=AUDIO_MODE,
                          csn=AUDIO_CSN, sclk=AUDIO_SCLK, sdin=AUDIO_SDIN)
    # Internal audio bus
    au_bus = Namespace(in_r=au_in_r, in_l=au_in_l, out_r=au_out_r, out_l=au_out_l,
                       mic_in=mic_in, hp_out=hp_out, Ts=Ts)    

    clk12MHz = Signal(False); 
    clk48MHz = Signal(False); 
    clk96MHz = Signal(False)
    dcm_locked = Signal(False)
    _clock = Signal(False)

    one = Signal(True)
    zero = Signal(False)

    # Xilinx DCM IP, generate clocks required.
    g_dcm = dcm12MHz(CLKIN_IN=clock_in, RST_IN=zero, CLKDV_OUT=clk12MHz,
                     CLKIN_IBUFG_OUT=_clock, CLK0_OUT=clk48MHz,
                     CLKFX_OUT=clk96MHz, LOCKED_OUT=dcm_locked)

    rbits = Signal(intbv(0)[8:])
    @always(_clock.posedge, reset_in.negedge)
    def hdl_reset():
        if reset_in == 0:
            rbits.next = 0
            reset.next = 0
        else:
            rbits.next = ((rbits << 1) | 1) & 0xFF
            reset.next = rbits[7]
            
    # The logic to interface to the AIC23 CODEC
    if ConfigOpt is None:
        ConfigOpt = Aic23Config()
        ConfigOpt.sample_rate = 48   # 48kHz sample rate
        ConfigOpt.input_len = 16     # 16bit samples

    g_aic23 = aic23(clock=clk96MHz, 
                    reset=reset, 
                    au_bus=au_bus, 
                    aic23_bus=aic23_bus, 
                    tst_pts=tst_pts, 
                    ConfigOpt=ConfigOpt)


    @always(clk96MHz.posedge)
    def hdl_loopback():
        au_out_r.next = au_in_r
        au_out_l.next = au_in_l

    cnt = Signal(modbv(0)[32:])
    @always_seq(clk12MHz.posedge, reset=reset)
    def hdl_cnt():
        cnt.next = cnt+1

    @always_seq(clk48MHz.posedge, reset=reset)
    def hdl_leds():
        LEDS.next = cnt[32:25]

    oclk = Signal(False)
    oclk_n = Signal(False)
    @always_comb
    def hdl_assigns():
        oclk.next = clk12MHz
        oclk_n.next = not clk12MHz

    # Xilinx DDR IO to send 12MHz clock to AIC23 CODEC
    g_ddr = OFDDRCPE(Q=AUDIO_CLK, C0=oclk, C1=oclk_n, CE=one, 
                     CLR=zero, D0=one, D1=zero, PRE=zero)

    return g_aic23, g_dcm, hdl_loopback, hdl_cnt, hdl_leds, hdl_reset, hdl_assigns, g_ddr


def _convert(ConfigOpt):
    clock        = Signal(False)
    reset        = ResetSignal(False, active=0, async=True)
    AUDIO_CLK    = Signal(False)
    AUDIO_BCLK   = Signal(False)
    AUDIO_DIN    = Signal(False)       
    AUDIO_DOUT   = Signal(False)      
    AUDIO_LRCIN  = Signal(False)     
    AUDIO_LRCOUT = Signal(False)    
    AUDIO_MODE   = Signal(False)      
    AUDIO_CSN    = Signal(False)       
    AUDIO_SCLK   = Signal(False)       
    AUDIO_SDIN   = Signal(False)
    tst_pts      = Signal(intbv(0)[8:])
    LEDS         = Signal(intbv(0)[7:])

    toVerilog(aic23_top, clock, reset, AUDIO_CLK, AUDIO_BCLK, AUDIO_DIN, AUDIO_DOUT,
              AUDIO_LRCIN, AUDIO_LRCOUT, AUDIO_MODE, AUDIO_CSN,
              AUDIO_SCLK, AUDIO_SDIN, tst_pts, LEDS)

    # ??? The stub code in xip.OFDDRCPE cause and "no proper edge test"?
    #toVHDL(aic23_top, clock, reset, AUDIO_CLK, AUDIO_BCLK, AUDIO_DIN, AUDIO_DOUT,
    #       AUDIO_LRCIN, AUDIO_LRCOUT, AUDIO_MODE, AUDIO_CSN,
    #       AUDIO_SCLK, AUDIO_SDIN, tst_pts, LEDS)


def _create_parser():
    parser = None
    return parser

if __name__ == '__main__':
    _convert(Aic23Config(_create_parser()))

    
