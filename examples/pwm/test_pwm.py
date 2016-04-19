
import os
import glob
import shutil
import csv
from math import sin, fmod, pi
import argparse

from myhdl import *
from myhdl_tools import Clock,Reset
from pwm import m_pwm

description = \
""" Run a pwm simulation with a tone input.
"""

def test_pwm(args):
    
    fn = args.fn
    N = args.N
    Fsine = args.Fsine
    args.trace=True
    Fpwm = 32e3      # Desired PWM frequency    37.5e3 for Fs=48e6
    Fclock = 48e6    # FPGA main clock frequency
    xnbits = 10      # number of bits for the PWM
    Xmax,Xmin = (2**(xnbits-1),-1*2**(xnbits-1))

    # declare the interface signals
    clock = Clock(0, frequency=Fclock)
    reset = Reset(0, active=0, async=False)  # For FPGA simply use a sync reset, see ...
    x = Signal(intbv(0, min=Xmin, max=Xmax))
    y = Signal(bool(0))
    ts = Signal(bool(0))

    if args.trace:
        tb_dut = traceSignals(m_pwm, clock, reset, x, y, ts,
                              pwm_frequency=Fpwm)
    else:
        tb_dut = m_pwm(clock, reset, x, y, ts,
                     pwm_frequency=Fpwm)
        
    Hclk = 12  # period Hclk sim ticks
    Sdly = 4   # how often to collect samples 4x Fclock
    Fs = clock.frequency * (2.*Hclk)/float(Sdly)
    print('   Simulation sample rate %.3fkHz' % (Fs/1e3))
    tb_clock = clock.gen(hticks=Hclk)
                   
    # time-steps in nanoseconds
    Tsim = 1/(Fs) * 1e9
    @instance
    def tb_stimulus():
        print('   Start sine PWM')
        phid = (Fsine/Fs)*2*pi
        phia = 0.
        yield reset.pulse(100)
        nn = 0
        yield clock.posedge
        
        with open(fn, 'wb') as csvfile:            
            cw = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            xint,xin = 0,0
            print('   start saving samples to file')
            while nn < N:
                # each simulation step is 6*ClockFreq, create a 
                # current values
                t = Tsim*now()
                xs = sin(phia)*(x.max-1)
                cw.writerow(["%.3f"%(t), "%.7f"%(xs), str(xin), str(int(y))])
                # next values
                phia = fmod(phia+phid, 2*pi)
                xint = int(round(sin(phia)*(x.max-1)))
                if xint >= x.max : xint = x.max-1
                if xint <= x.min : xint = x.min
                x.next = xint
                
                # is this one of the captured points (PWM period)
                if ts:
                    nn += 1
                    xin = int(x)  # the PWM is only 10bits 
                    if nn%8192 == 0 :
                        print('   ... progress %d' % (nn))

                yield delay(Sdly)  # Fclock*(2*Hclk/Sdly) sample rate
           
        print('   End sine PWM')
        raise StopSimulation
        
    return tb_dut, tb_clock, tb_stimulus


if __name__ == '__main__':
    # This simulation is typically run with pypy and the
    # resulting data vectors are analyzed with ipython
    parser = argparse.ArgumentParser(description="a pwm simulation with a tone input")
    parser.add_argument("-N", type=int, default=1024,
                        help="number of x input samples to simulate")
    parser.add_argument("--trace", action="store_true",
                        help="enable simulation tracing")
    parser.add_argument("--clean", action="store_true",
                        help="delete previous generated files")
    args = parser.parse_args()    

    print(args)
    # delete all the generated files
    if args.clean:
        fcsv = glob.glob("*.csv")
        for ff in fcsv:
            print('remove %s' % (ff))
            os.remove(ff)
        fvcd = glob.glob("*.vcd*")
        for ff in fvcd:
            print('remove %s' % (ff))
            os.remove(ff)

    SineFreq = [1e3, 9e3, 15e3]    
    for ff in SineFreq:
        args.fn = 'pwm_samples_%dkHz_tone_N%d.csv'%(int(round(ff/1e3)),args.N)
        print('  [%fHz]  ' % (ff))
        args.Fsine = ff
        Simulation(test_pwm(args)).run()
        if args.trace:
            shutil.move('m_pwm.vcd', 'pwm_%dkHz_tone_N%d.vcd'%(int(round(ff/1e3)),args.N))
