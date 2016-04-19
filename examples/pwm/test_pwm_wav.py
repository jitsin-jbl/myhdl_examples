
from myhdl import *
import csv
from pprint import pprint

from kr.blocks import Block
from kr.blocks import Clock, Reset
from kr.blocks import GetAllGenerators
from kr.blocks.sources import WaveReader
from kr.blocks.sinks import WaveWriter
from kr.blocks.filters import MovingAverage

from pwm import m_pwm


def test_pwm_wave(fn='samples_wav.csv'):
    Fpwm = 32e3    # PWM frequency (period)
    Fclock = 48e6  # System clock frequency

    # Global system sources
    bclk = Clock(frequency=48e6, system_clock=True)
    brst = Reset(system_reset=True)
    clock = bclk.clock
    reset = brst.reset
    pprint(vars(bclk))
    pprint(vars(clock))
    y = Signal(bool(0))

    ts_pwm = Signal(bool(0)) # sample strobe from PWM
    ts_flt = Signal(bool(0)) # sample strobe from filter
    
    # Block sources
    bwavi = WaveReader(clock=clock, reset=reset, ts=ts, 
                      filename='first_snip.wav')
    x = bwavi.GetOutputSignal(0).signal
    bflt = MovingAverage(y, clock=clock, reset=reset, ts=ts_flt,N=1024)
    bwavo = WaveWriter(clock=clock, reset=reset, ts=ts,
                       filename='first_snip_out.wav')
    
    print('x from the Wave source type %s, min %d max %d' % (type(x), x.min, x.max))

    # dut
    #tb_dut = traceSignals(pwm, clock, reset, x, y, ts, 
    #                      Fpwm=PwmFreq, Fclock=ClockFreq)
    tb_dut = m_pwm(clock, reset, x, y, ts,
                   pwm_frequency=Fpwm)

    

    Tsim = 1/(Fclock*6)
    @instance
    def tb_stim():        
        yield brst.Pulse(10)

        with open(fn, 'wb') as csvfile:
            cw = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            xint,xin = 0,0            
            while True:
                t = Tsim*now()
                cw.writerow(["%.3f"%(t), str(int(x)), str(int(ts)), str(int(y))])
                yield clock.posedge

    g = (tb_dut, bwav.gprocess(), bclk.gprocess(), brst.gprocess(), tb_stim)
    Simulation(g).run()


if __name__ == '__main__':
    test_pwm_wave()
