
from myhdl import *
from aic23_top import aic23_top
from aic23_config import Aic23Config
from i2s_model import i2s_model


def test_aic23():
    
    cfgopt = Aic23Config()
    cfgopt.input_len = 16
    cfgopt.sample_rate = 48

    clock           = Signal(False)
    reset           = ResetSignal(True, active=0, async=True)

    # AIC23 IC ports
    AUDIO_CLK       = Signal(False)
    AUDIO_BCLK      = Signal(False)
    AUDIO_DIN       = Signal(False)       
    AUDIO_DOUT      = Signal(False)      
    AUDIO_LRCIN     = Signal(False)     
    AUDIO_LRCOUT    = Signal(False)    
    AUDIO_MODE      = Signal(False)      
    AUDIO_CSN       = Signal(False)       
    AUDIO_SCLK      = Signal(False)       
    AUDIO_SDIN      = Signal(False)
    
    tst_pts         = Signal(intbv(0)[8:])
    LEDS = Signal(intbv(0)[7:])
    auir, auil = [Signal(modbv(0)[cfgopt.input_len:]) for ii in (0,1)]
    auor, auol = [Signal(modbv(0)[cfgopt.input_len:]) for ii in (0,1)]
    AuMax = (2**cfgopt.input_len)-1
    AuMin = -1*AuMax
    new_sample = Signal(False)

    def _test_aic():
        
        tb_i2s = i2s_model(AUDIO_LRCIN, AUDIO_LRCOUT, AUDIO_BCLK,
                           AUDIO_DIN, AUDIO_DOUT,
                           auir, auil, auor, auol, new_sample,
                           BitsPerLr=cfgopt.input_len)

        tb_dut = aic23_top(clock, reset, 
                           AUDIO_CLK, AUDIO_BCLK, AUDIO_DIN, AUDIO_DOUT, 
                           AUDIO_LRCIN, AUDIO_LRCOUT, AUDIO_MODE,
                           AUDIO_CSN, AUDIO_SCLK, AUDIO_SDIN, tst_pts, LEDS, 
                           ConfigOpt=cfgopt)

        @always(delay(2))
        def tb_clkgen():
            clock.next = not clock

        @always(delay(200))
        def tb_bclkgen():
            AUDIO_BLCK.next = not AUDIO_BCLK

        @instance
        def tb_stimulus():
            auir.next = AuMin
            auil.next = AuMax
            reset.next = False
            yield delay(100)
            reset.next = True
            yield clock.posedge

            for ii in range(333):
                yield new_sample.posedge
                auir.next = auir + 1
                auil.next = auil - 1

            raise StopSimulation
            
        return tb_stimulus, tb_clkgen, tb_i2s, tb_dut

    Simulation(traceSignals(_test_aic)).run()


if __name__ == '__main__':
    test_aic23()
