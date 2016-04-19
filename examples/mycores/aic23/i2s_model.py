

from myhdl import *

def i2s_model(
    lrcin,         # Input Left / Right select
    lrcout,        # Output Left / Right select
    bclk,          # Source data clock
    din,           # Data serial input  (into DAC)
    dout,          # Data serial output (out ADC)

    au_in_r,       # Parallel audio data
    au_in_l,       # Parallel audio data
    au_out_r,      # Parallel audio data
    au_out_l,      # Parallel audio data
    new_sample,   # New samples ready and au_in_* has been read

    # Model Parameters
    BitsPerLr = 32,
    BclkPeriod = 20
    ):
    """ I2S audio mode
    """
    
    LrMaxCnt = BitsPerLr + 1
    lrcnt = Signal(intbv(0, max=LrMaxCnt))

    pdata = Signal(intbv(0)[LrMaxCnt:])
    sdata = Signal(intbv(0)[LrMaxCnt:])
    
    THbclk = BclkPeriod/2
    @always(delay(THbclk))
    def rtl_bclk_gen():
        bclk.next = not bclk

    @always(bclk.negedge)
    def rtl_lr_gen():
        if lrcnt ==  BitsPerLr:
            lrcnt.next = 0
            lrcin.next  = not lrcin
            lrcout.next = not lrcout
        else:
            lrcnt.next = lrcnt + 1

    _lrcout = Signal(False)
    _lrcin  = Signal(False)
    @always(bclk.negedge)
    def rtl_data_gen():
        _lrcout.next = lrcout
        _lrcin.next  = lrcin

        if lrcout and not _lrcout:
            pdata.next = au_in_r
            new_sample.next = False
        elif not lrcout and _lrcout:
            pdata.next = au_in_l
            new_sample.next = True
        else:
            pdata.next = (pdata << 1) & ((2**BitsPerLr)-1)
            new_sample.next = False

    @always(bclk.posedge)
    def rtl_in():
        sdata.next = concat(sdata[BitsPerLr-2:0], din)
        
    @always_comb
    def rtl_out():
        dout.next = pdata[BitsPerLr-1]

    return instances()
    

    

    
