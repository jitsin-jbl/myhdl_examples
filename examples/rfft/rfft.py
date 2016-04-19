#
# Copyright (c) 2011 Christopher Felton
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
"""

from random import randrange

import sys,os,time

from math import log, pi, ceil, sqrt

import numpy as np
from myhdl import *

# Additional testing with pypy 1.6, don't think MPL is supported
# by pypy, yet.
try:
    import pylab as plt
    PLOT_OK = True
except:
    PLOT_OK = False

#import cProfile as profile
#import pstats

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def genSinArray(N=8, w=8, p=0):
    """
    Generate a Sine Wave
      N  -- Number of points to return
      w  -- samples per period, angular frequency w = 
      p  -- phase
    """
    n = np.array(range(N, 0, -1))
    x = np.cos(2*pi*n/w + p)

    return x;

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def genSinArrayF(N=8, F=1000, Fs=8000, phi=0):
    """
    Generate a Sine Wave
      N  -- Number of points to return
      F  -- The frequency of the sine wave
      Fs -- Discrete sampling rate.
    """
    Ts = 1.0/Fs
    t = np.array(range(0, N) * Ts)
    x = np.sin(t*2*pi*F + phi)
    return x;

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getTwiddle(NFFT=8):
    """Generate the \"Twiddle Factors\" """
    W = np.array([1. for ii in range(NFFT)], complex)
    #print("Twiddles len %d %s" % (len(W), str(W)))
    for k in range(NFFT):
	W[k] = np.cos(2.0*pi*k/NFFT) - 1.0j*np.sin(2.0*pi*k/NFFT)

        #if abs(real(W[k])) < 10**-6:
        #    W[k] = 0. + W[k].imag
        #if abs(imag(W[k])) < 10**-6:
        #    W[k] = W[k].real + 0.j            

    return W

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def myFFTRr2(x):
    """
    This is a recursive FFT, this is a model for the HDL version.

    Resources
      -- http://www.cse.uiuc.edu/iem/fft/rcrsvfft/
      -- \"A Simple and Efficient FFT Implementation in C++\"
          by Vlodymyr Myrnyy
    """
    
    n = len(x)

    if (n == 1):
	return x

    w = getTwiddle(n)
    m = n/2;
    X = np.ones(m, complex)
    Y = np.ones(m, complex)
    
    for k in range(m):
        X[k] = x[2*k]
        Y[k] = x[2*k + 1] 

    X = myFFTRr2(X)  # w**2
    Y = myFFTRr2(Y)  # w**2

    F = np.ones(n, complex)
    for k in range(n):
        i = (k%m)
        F[k] = X[i] + (w[k] * Y[i])

    return F


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def fft_mult(x1,x2,y, Q):

    @always_comb
    def rtl():
        y.next = (x1 * x2) >> Q

    return rtl

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def dataValid(dvl, dv_o):

    @always_comb
    def rtl():
        dv_o.next = dvl[0]

    return rtl

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def butterfly(
    clk,
    rst,
    xr,
    xi,
    yr,
    yi,
    wr,
    wi,
    Zxr,
    Zxi,
    Zyr,
    Zyi,
    Q):
    """
    @todo: generic butterfly
    """
    L = 2**Q
    mr = Signal(intbv(0, min=-L, max=L))
    mi = Signal(intbv(0, min=-L, max=L))

    
    # TODO add multiply modules
    @always(clk.posedge)
    def rtl():
        if rst :
            zr.next = 0
            zi.next = 0
        else:
            #print xr,xi, yr,yi, wr,wi
            zr.next = xr + (wr * yr - wi * yi)
            zi.next = xi + (wr * yi + wi * yr)

    return rtl
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def twiddle(
    clk,       #  
    rst,       # Sync Reset
    xr, xi,    # First set of inputs
    yr, yi,    # Second set of inputs
    wr, wi,    # Twiddle Factors
    zr, zi,    # Outputs
    dv_i,      #
    dv_o,      #
    Q          # 
    ):
    """

    """
    
    #m0 = Signal(
    @always(clk.posedge)
    def rtl():
        if rst :
            zr.next = 0
            zi.next = 0
        else:
            zr.next = xr + ((wr * yr - wi * yi) >> Q)
            zi.next = xi + ((wr * yi + wi * yr) >> Q)
            dv_o.next = dv_i
    return rtl

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def feedthru(clk, rst, xr, xi, zr, zi, dv_i, dv_o):
    """
    Output Register Stage
    """

    @always(clk.posedge)
    def rtl():
        if rst:
            zr.next = 0
            zi.next = 0
        else:
            zr.next = xr
            zi.next = xi

    return rtl

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def fft_core(
    clk,      # 
    rst,      #
    xr,       # Real input list of signals
    xi,       # Imaginary input list of signals
    zr,       # Real output list of signals
    zi,       # Imaginary output list of signals
    dv_i,     # Data Valid input (start FFT)
    dv_o,     # Data Valid output 
    Q=8):
    """
        x  --  List of Signals
        w  --  List of Ints (Tuple of Ints?)
        z  --  List of Signals output
        Nfft -- 
    """
    
    
    n = len(xr)

    #if len(xr) != Nfft or len(xi) != Nfft:
    #    print 'Input Size Error xr len(xr) %d, len(xi) %d, Nfft %d' % (len(xr), len(xi), Nfft) 
    
    m = n/2;
    L = 2**(Q + int(log(n,2)) )
    
    comp  = [None for i in range(n)]
    
    if m > 0:
        Xir   = [Signal(intbv(0, min=-L, max=L)) for i in range(m)]
        Xii   = [Signal(intbv(0, min=-L, max=L)) for i in range(m)]
        Yir   = [Signal(intbv(0, min=-L, max=L)) for i in range(m)]
        Yii   = [Signal(intbv(0, min=-L, max=L)) for i in range(m)]
        Xor   = [Signal(intbv(0, min=-L, max=L)) for i in range(m)]
        Xoi   = [Signal(intbv(0, min=-L, max=L)) for i in range(m)]
        Yor   = [Signal(intbv(0, min=-L, max=L)) for i in range(m)]
        Yoi   = [Signal(intbv(0, min=-L, max=L)) for i in range(m)]
        dvl   = [Signal(intbv(0)[1:]) for i in range(n)]

    dv_o1 = Signal(intbv(0)[1:])
    dv_o2 = Signal(intbv(0)[1:])
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Next twiddles
    Wr    = [0]*n
    Wi    = [0]*n
    Wn = getTwiddle(n)
    for i in range(n):
        Wr[i] = int(round(Wn[i].real * 2**Q)) 
        Wi[i] = int(round(Wn[i].imag * 2**Q)) 

    Wr = tuple(Wr)
    Wi = tuple(Wi)

        
    ##  HDL Generation
    if n > 1:
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Split even and odd
        for k in range(m):
            Xir[k] = xr[2*k]
            Xii[k] = xi[2*k]
            Yir[k] = xr[2*k + 1]
            Yii[k] = xi[2*k + 1] 

        fft1 = fft_core(clk, rst, Xir, Xii, Xor, Xoi, dv_i, dv_o1, Q)
        fft2 = fft_core(clk, rst, Yir, Yii, Yor, Yoi, dv_i, dv_o2, Q)
        for k in range(n):
            i = (k%m)
            # Select different twiddle kernels
            comp[k] = twiddle(clk, rst, Xor[i], Xoi[i], Yor[i], Yoi[i],
                              Wr[k], Wi[k], zr[k], zi[k], dv_o1, dvl[k], Q)
            dv = dataValid(dvl, dv_o)
            # TODO add Butterfly, it will be more efficient, the butterfly
            #           will return 2 values, logic will have to change some.
        return fft1, fft2, comp, dv
    else:
        feed = feedthru(clk, rst, xr[0], xi[0], zr[0], zi[0], dv_i, dv_o)
        return feed

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def fft_core_N8(clk, rst,
                xr0, xr1, xr2, xr3, xr4, xr5, xr6, xr7,
                xi0, xi1, xi2, xi3, xi4, xi5, xi6, xi7,
                Xr0, Xr1, Xr2, Xr3, Xr4, Xr5, Xr6, Xr7,
                Xi0, Xi1, Xi2, Xi3, Xi4, Xi5, Xi6, Xi7,
                Q=7):
    """
    Need a small wrapper for each order FFT that will be converted to Verilog/VHDL.
    """

    top_mod = fft_core(clk, rst,
                       [xr0, xr1, xr2, xr3, xr4, xr5, xr6, xr7],
                       [xi0, xi1, xi2, xi3, xi4, xi5, xi6, xi7],
                       [Xr0, Xr1, Xr2, Xr3, Xr4, Xr5, Xr6, Xr7],
                       [Xi0, Xi1, Xi2, Xi3, Xi4, Xi5, Xi6, Xi7])

    return top_mod
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def genFFT_N8(Q=7):
    """

    """
    N = 8
    L=2**Q
    
    clk = Signal(False)
    rst = Signal(False)
    
    Xr0 = Signal(intbv(0, min=-L, max=L))
    xr1 = Signal(intbv(0, min=-L, max=L))
    xr2 = Signal(intbv(0, min=-L, max=L))
    xr3 = Signal(intbv(0, min=-L, max=L))
    xr4 = Signal(intbv(0, min=-L, max=L))
    xr5 = Signal(intbv(0, min=-L, max=L))
    xr6 = Signal(intbv(0, min=-L, max=L))
    xr7 = Signal(intbv(0, min=-L, max=L))

    xi0 = Signal(intbv(0, min=-L, max=L))
    xi1 = Signal(intbv(0, min=-L, max=L))
    xi2 = Signal(intbv(0, min=-L, max=L))
    xi3 = Signal(intbv(0, min=-L, max=L))
    xi4 = Signal(intbv(0, min=-L, max=L))
    xi5 = Signal(intbv(0, min=-L, max=L))
    xi6 = Signal(intbv(0, min=-L, max=L))
    xi7 = Signal(intbv(0, min=-L, max=L))

    Xr0 = Signal(intbv(0, min=-N*L, max=N*L))
    Xr1 = Signal(intbv(0, min=-N*L, max=N*L))
    Xr2 = Signal(intbv(0, min=-N*L, max=N*L))
    Xr3 = Signal(intbv(0, min=-N*L, max=N*L))
    Xr4 = Signal(intbv(0, min=-N*L, max=N*L))
    Xr5 = Signal(intbv(0, min=-N*L, max=N*L))
    Xr6 = Signal(intbv(0, min=-N*L, max=N*L))
    Xr7 = Signal(intbv(0, min=-N*L, max=N*L))

    Xi0 = Signal(intbv(0, min=-N*L, max=N*L))
    Xi1 = Signal(intbv(0, min=-N*L, max=N*L))
    Xi2 = Signal(intbv(0, min=-N*L, max=N*L))
    Xi3 = Signal(intbv(0, min=-N*L, max=N*L))
    Xi4 = Signal(intbv(0, min=-N*L, max=N*L))
    Xi5 = Signal(intbv(0, min=-N*L, max=N*L))
    Xi6 = Signal(intbv(0, min=-N*L, max=N*L))
    Xi7 = Signal(intbv(0, min=-N*L, max=N*L))

    toVerilog(fft_core_N8, clk, rst,
              xr0, xr1, xr2, xr3, xr4, xr5, xr6, xr7,
              xi0, xi1, xi2, xi3, xi4, xi5, xi6, xi7,
              Xr0, Xr1, Xr2, Xr3, Xr4, Xr5, Xr6, Xr7,
              Xi0, Xi1, Xi2, Xi3, Xi4, Xi5, Xi6, Xi7)

    toVHDL(fft_core_N8, clk, rst,
              xr0, xr1, xr2, xr3, xr4, xr5, xr6, xr7,
              xi0, xi1, xi2, xi3, xi4, xi5, xi6, xi7,
              Xr0, Xr1, Xr2, Xr3, Xr4, Xr5, Xr6, Xr7,
              Xi0, Xi1, Xi2, Xi3, Xi4, Xi5, Xi6, Xi7)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def cmdLineTestBench(run='run', N=128, Q=23):
    """
    """
    L=2**Q

    clk = Signal(False)
    rst = Signal(False)

    dv_i  = Signal(intbv(0)[1:])
    dv_o = Signal(intbv(0)[1:])
    
    xr  = [Signal(intbv(0, min=-L-1, max=L+1)) for i in range(N)]
    xi  = [Signal(intbv(0, min=-L-1, max=L+1)) for i in range(N)]

    Xr  = [Signal(intbv(0, min=-N*L, max=N*L)) for i in range(N)]
    Xi  = [Signal(intbv(0, min=-N*L, max=N*L)) for i in range(N)]

    if run == 'trace':
        dut = traceSignals(fft_core, clk, rst, xr, xi, Xr, Xi, dv_i, dv_o, Q)
    else:
        dut = fft_core(clk, rst, xr, xi, Xr, Xi, dv_i, dv_o, Q)

    # Clock Generation
    @always(delay(1))
    def clkgen():
        clk.next = not clk


    nstart   = 4          # Note Aliased signal included
    nstep    = 4          # samples per period step
    pstep    = pi/4       # Phase step size
    limErr   = 2          # Error limit to check
    maxErr   = 0          # max difference
    
    @instance
    def stimulus():
        TEST1 = False
        print 'Start TestBench'
        maxErr = 0
        zFFT   = [None]*N
        zFFTP  = np.zeros(N)
        yield clk.posedge
        rst.next = 1
        yield delay(10)
        rst.next = 0
        yield delay(10)
        
        if TEST1:
            yield(clk.negedge)
            xin  = [1,-1,1,-1]
            xFFT = myFFTRr2(xin)
            for i in range(N):
                xr[i].next = int(xin[i] * L)
                xi[i].next = 0
            yield(delay(80))
            yield(clk.negedge)
            print Xr
            print Xi
        else:
            # pypy numpy support is limited, no arange that
            # supports float steps
            ub = (pi+pstep) / pstep
            print("ub %f / %d" % (ub, ceil(ub)))
            pList = list(np.array(range(0, int(ub))) / pstep)
            for s in range(nstart, N+nstep, nstep):
                for p in pList:
                    yield(clk.negedge)
                    xin  = genSinArray(N, s, p)
                    xFFT = myFFTRr2(xin)
                    # Compare Output To Original
                    for i in range(N):
                        xr[i].next = int(xin[i] * L)
                        xi[i].next = 0

                    yield(delay(80))

                    for i in range(N):
                        zFFT[i] = (float(Xr[i]) + float(Xi[i])*1j)/L

                    for i in range(N):
                        zFFTP[i] = round(np.abs(zFFT[i]), 3)
                    
                    rmsErr = sqrt(np.mean(np.abs(np.array([zFFT]) - np.array([xFFT]) ))**2)

                    if rmsErr > limErr:
                        print "Error!", rmsErr
                        raw_input('Error try again')
                    else:
                        if PLOT_OK:
                            plt.ioff()
                            plt.plot(zFFTP)
                            plt.plot(np.round(np.array([np.abs(xFFT)]), 3), '--r')
                            plt.savefig('plots/my_fft_N%d_s%d_p%d.png' % (N,s,p))
                            plt.close('all')
                        else:
                            print xFFT

                    if rmsErr > maxErr:
                        maxErr = rmsErr
                        zFFTErr = zFFT
                        xFFTErr = xFFT

                    print 'Max RMS Error = ', maxErr
                    for i in range(N):
                        xFFTErr[i] = round(abs(xFFTErr[i]), 3)
                        zFFTErr[i] = round(abs(zFFTErr[i]), 3)
                    #print xFFTErr
                    #print zFFTErr
        
        raise StopSimulation

    return clkgen, stimulus, dut


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run from script
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    tb = cmdLineTestBench(sys.argv[1])
    
    if sys.argv[1] != 'ver':
        sim = Simulation(tb)
        print '-'*80
        print time.localtime()
        sim.run()
        print time.localtime()
        print '-'*80
    if sys.argv[1] == 'ver':
        genFFT_N8()
