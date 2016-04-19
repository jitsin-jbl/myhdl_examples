from myhdl import *

from aic23 import aic23

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


def aic23_top(
    # --[System Signals]--
    clock,   # also known as fclk
    reset,   # system reset
    
    # --[ Wishbone Bus ]--
    clk_i,          # wishbone clock
    rst_i,          # wishbone reset 
    cyc_i,          # cycle
    stb_i,          # strobe
    adr_i,          # address
    we_i,           # write enable
    sel_i,          # byte select
    dat_i,          # data input
    dat_o,          # data output
    ack_o,          # acknowledge

    
    # --[ CODEC interface to FPGA logic (audio stream) ]--
    au_in_r,     # Output: audio in stream to FPGA logic right channel
    au_in_l,     # Output: audio in stream to FPGA logic left channel
    au_out_r,    # Input:  audio out stream from FPGA logic right channel
    au_out_l,    # Input:  audio out stream from FPGA logic left channel
    mic_in,      # Input:  Mic audio stream
    hp_out,      # Output: Speaker audio stream
    Ts,          # Output: Sample rate pulse
    
    # --[ External CODEC interface to AIC23, see pinout above comments ]--
    #AUDIO_CLK,      # Output:   This is driven by top-level DCM->DDR flop 
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

    # --[ Parameters ]--
    C_WB_ADDR = 0x1000
    ):
    """AIC23 interface
    This module contains the logic to configure the AIC23 in a default mode
    and transfer audio to and fro.
    """

    fclk = clock


    
