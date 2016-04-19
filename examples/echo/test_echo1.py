#
# Copyright (c) 2008-2012 Christopher L. Felton
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

import sys
from math import pi, sin

from myhdl import *
from echo1 import echo1

try:
    from pylab import *
    USE_PLOT = True
except:
    print("no plotting")
    USE_PLOT = False

# globals used by all tests
Nbits = 24
SampMax = 2**(Nbits-1)-1
SampMin = -1*(2**(Nbits-1)-1)

clock = Signal(False)
reset = Signal(False)
au_fs = Signal(True)
au_in = Signal(intbv(0, max=SampMax, min=SampMin))
au_out = Signal(intbv(0, max=SampMax, min=SampMin))

Fs  = 48000   # Sample rate
#BD  = 32      # Buffer Depth

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_echo1_delay(BD=32, SimType='trace', InputSignal='pulse'):
    """Audio Echo Testbench

    This testbench will supply a basic signal to the audio echo module and
    verify that the output is delayed as expected.  A plot will also be
    generated.
    """
    
    # Design Under Test, instantiate the echo1 module
    SampleRate = 48000
    if SimType.lower() == 'trace':
        dut = traceSignals(echo1, clock, reset, au_fs, au_in, au_out, 
                           C_BD=BD,    # BufferDepth
                           C_BW=16,    # BufferWordWidth
                           C_SR=48000, # SampleRate
                           C_SW=24)    # SampleWordWidth
    else:
        dut = echo1(clock, reset, au_fs, au_in, au_out, 
                    C_BD=BD,    # BufferDepth
                    C_BW=16,    # BufferWordWidth
                    C_SR=48000, # SampleRate
                    C_SW=24)    # SampleWordWidth
    npts = 4096
    svi = [0 for ii in range(npts)]  # signal vector input
    svo = [0 for ii in range(npts)]  # signal vector output

    #         InputSignal = ['impulse', 'sine']
    if InputSignal.lower() == 'pulse':
        plsi  = int(BD*0.08) # pulse index
        svi[plsi]   = int(SampMax/4)
        svi[plsi+1] = int(SampMin/4)
    elif InputSignal.lower() == 'sine':
        Fs = 48000.; F= 33.
        t = [1/Fs*nn for nn in range(npts)]
        svi = [int(sin(2*pi*F*ii)*SampMax/4.) for ii in t]
    else:
        raise StandardError("Invalid InputSignal type %s" % (InputSignal))

    @always(delay(2))
    def tb_clkgen():
        clock.next = not clock

    clkcnt = 0
    @always(clock.posedge)
    def tb_fsgen():
        global clkcnt
        if au_fs:
            clkcnt = 0
            au_fs.next = False
        elif clkcnt >= 16:
            au_fs.next = True
        else:
            clkcnt += 1
            
    @instance
    def tb_stimulus():
        reset.next = False
        for ii in range(3):
            yield au_fs.posedge
        reset.next = True
        for ii in range(3):
            yield au_fs.posedge
        #au_in.next = int(svi[0])
        for iis in xrange(len(svi)):
            au_in.next = int(svi[iis])
            yield au_fs.posedge
            svo[iis] = int(au_out)


        # Only checking that the expected delay is non-zero
        if InputSignal.lower() == 'impulse':
            assert svo[plsi+BD] > 0,   '1 Echo failed svo[%d] == %d' % (plsi+BD, svo[plsi+BD])
            assert svo[plsi+BD+1] < 0, '2 Echo failed svo[%d] == %d' % (plsi+BD+1, svo[plsi+BD+1])
        
        if USE_PLOT:
            ioff()
            mfmt = 'o' if InputSignal.lower() == 'pulse' else ''
            if BD <= 32:
                psvi = svi[:BD*4]
                psvo = svo[:BD*4]
                stem(arange(len(psvi)), psvi, linefmt='b', markerfmt='b'+mfmt, basefmt=' ', hold=True)
                title('Buffer Length %s' % (BD))
                savefig('echo1_plot_stem_%s_%s_svi_only.png'%(InputSignal, BD))
                stem(arange(len(psvo)), psvo, linefmt='g', markerfmt='g'+mfmt, basefmt=' ', hold=True)
                title('Buffer Length %s' % (BD))
                savefig('echo1_plot_stem_%s_%s.png'%(InputSignal, BD))
                close('all')

            mrk = '.' if InputSignal.lower() == 'pulse' else ''
            plot(svi, marker=mrk)
            plot(svo, marker=mrk)
            xlabel('Samples')
            title('Buffer Length %s' % (BD))
            savefig('echo1_plot_%s_%s.png'%(InputSignal, BD))
            close('all')

        raise StopSimulation

    return tb_stimulus, tb_clkgen, tb_fsgen, dut



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    if len(sys.argv) == 2:
        InputSignal = sys.argv[1]
    else:
        InputSignal = 'pulse'

    for ii in range(3,13):
        Simulation(test_echo1_delay(BD=2**ii, 
                                    SimType='run', 
                                    InputSignal=InputSignal)).run()
