
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
    Fsine = [1e3, 9e3, 15e3]
    
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
        phid = []
        for sn in Fsine:
            pd = (sn/Fs)*2*pi
            phid.append(pd)
        phia = [0.,0.,0.]
        
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
                xs = 0
                for iphia in phia:
                    xs += (sin(iphia)/3.)*(x.max-1)
                cw.writerow(["%.3f"%(t), "%.7f"%(xs), str(xin), str(int(y))])
                # next values
                for ac,dp in zip(phia,phid):
                    ac = fmod(ac+dp, 2*pi)
                xint = int(round(xs))
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
                #yield clock.posedge            
           
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
    args.trace=True
    print(args)
    args.fn = 'samples_tones_N%d_tri.csv'%(args.N)
    Simulation(test_pwm(args)).run()
    if args.trace:
        shutil.move('m_pwm.vcd', 'pwm_tones_N%d_tri.vcd'%(args.N))
