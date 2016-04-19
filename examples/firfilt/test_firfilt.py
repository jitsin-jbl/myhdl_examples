import sys
import os
import argparse
from argparse import Namespace

from myhdl import *
from myhdl_tools import Reset,Clock

import numpy as np
from numpy import pi, log10
from scipy import signal
from matplotlib import pyplot as plt
from matplotlib import mlab
import cPickle

# various forms of a FIR filter
from firfilt import m_firfilt

# more often than not the clock rate is not equal to
# the clock rate.
class SignalStream(object):
    def __init__(self, stype):
        self.val = Signal(stype)
        self.dv = Signal(bool(0))


def test_firfilt(args):
    # what word size do we want?  Pick any size/
    sMax = 2**15; sMin=-1*sMax

    # Get the filter coefficients and plot the response
    coef = signal.fir_filter_design.firwin(args.Nflt, args.Fc)
    icoef = map(int, coef*sMax)
    w,H = signal.freqz(coef)
    fig1,ax1 = plt.subplots(1)
    ax1.plot(w, 20*log10(abs(H)))
    ax1.grid(True)
        
    sig_in = Signal(intbv(0, min=sMin, max=sMax))
    sig_out = Signal(intbv(0, min=sMin, max=sMax))
    clock = Clock(0, frequency=args.Fs)
    reset = Reset(False, active=1, async=False)

    def _test_firfilt():
        x,y = (sig_in,sig_out,)
        if args.trace:
            tb_dut = traceSignals(m_firfilt,clock,reset,x,y,icoef)
        else:
            tb_dut = m_firfilt(clock,reset,x,y,icoef)
        tb_clk = clock.gen(hticks=5)
        
        @instance
        def tb_stimulus():
            # pulse the reset
            yield reset.pulse(100)
            for ii in xrange(2):
                yield clock.posedge
                
            # chirp 1 (time response pictoral)
            print("   chirp 1 ...")
            samp_in = signal.chirp(np.arange(args.Nsamps/2)*1/args.Fs,
                                   8, .64, 480,
                                   method=u'logarithmic')*.94
            samp_in = np.concatenate(
                (samp_in,
                 np.array([ss for ss in reversed(samp_in[:-1])] )))
            samp_out = []
            fsamp_out=[]
            # input samples, save the output
            for ii in xrange(args.Nsamps-1):
                sig_in.next = int(np.floor(samp_in[ii]*(sMax)))
                yield clock.posedge
                samp_out.append(sig_out//float(sMax))
                fsamp_out.append(int(np.floor(samp_in[ii]*(sMax))))
            samp_out = np.array(samp_out)
            #fsamp_out = np.array(fsamp_out)
            #fsamp_out.save('fsamp_out.dat')
            fh=open('fsamp_out.dat','w')
            cPickle.dump(fsamp_out,fh)
            c = signal.lfilter(coef, 1, samp_in)
            sdiff = np.abs(c[:-2] - samp_out[2:])
            plt.figure(3); plt.plot(sdiff)
            #print(np.max(sdiff), np.mean(sdiff**2))
            #assert np.max(sdiff) < 1e-3, "error too large" 
            assert np.max(sdiff) > 1e-3, "error too large" 
            ia = np.concatenate((np.ones(args.Nflt/2)*.98, samp_in))
            fig,ax = plt.subplots(1)
            ax.plot(ia, 'b'); ax.plot(samp_out[1:], 'r'); ax.plot(c, 'y--')
            fig.savefig('__plot2.png')

            # chirp 2 (frequency response, more points)
            print("   chrip 2 ...")
            Nfft = 8*args.Nsamps
            samp_in = signal.chirp(np.arange(Nfft)*1/args.Fs,
                                   0.1, 1, 500)*.98
            samp_out = []
            for ii in xrange(Nfft):
                sig_in.next = int(np.floor(samp_in[ii]*(sMax)))
                yield clock.posedge
                samp_out.append(sig_out//float(sMax))
            samp_out = np.array(samp_out)
            Pi,fi = mlab.psd(samp_in)
            Po,fo = mlab.psd(samp_out)
            ax1.plot(pi*fi, 10*log10(abs(Po/Pi)), 'r')
            ax1.grid(True)
            fig1.savefig('__plot1.png')
            
            raise StopSimulation

        g = (tb_dut,tb_clk,tb_stimulus,)
        return g

    #if run.lower() == 'trace':
    #    tb_dut = traceSignals(firfilt, sig_in, sig_out, icoef, clk, rst)
    #elif run.lower() == 'cosim':
    #    if not os.path.isfile('firfilt.v'):
    #        raise StandardError('Run simulation first')
    #    if not os.path.isfile('myhdl.vpi'):
    #        raise StandardError('compile VPI interface')
    #    cmd = 'iverilog -o firfilt firfilt.v tb_firfilt_m.v'
    #    os.system(cmd)
    #    cmd = 'vvp -m ./myhdl.vpi firfilt'
    #    tb_dut = Cosimulation(cmd, sig_in=sig_in, sig_out=sig_out, 
    #                          icoef=icoef, clk=clk, rst=rst)
    #else:
    #    tb_dut = firfilt(sig_in, sig_out, icoef, clk, rst)
    #toVHDL(firfilt, sig_in, sig_out, icoef, clk, rst)
    #toVerilog(firfilt, sig_in, sig_out, icoef, clk, rst)

    print('run simulation')
    Simulation(_test_firfilt()).run()

    
if __name__ == '__main__':
    # @todo: _get_parser
    args = Namespace(Nsamps=1024,
                     Fs=1e3,
                     Nflt=33,
                     Fc=pi/17.,
                     trace=True)
    test_firfilt(args)    
