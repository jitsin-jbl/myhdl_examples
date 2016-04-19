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

"""
**********
Audio Echo
**********

The following is a testbench, RTL description, and conversion function for
an audio echo targetted for the DSPtronics Signa-X boards.  The audio echo
uses a fixed delay and uses internal BRAM to create the delay.

The testbench and converion function can be run by
  >> python echo1_convert.py

This will run the testbench, verify the dealy, create a plot, and create
the Verilog and VHDL.

After the Verilog and VHDL is generated they can be used in the Xilinx ISE
project supplied here.

More information available at
www.fpgarelated.com/
www.myhdl.org
"""

from myhdl import *
import math
from math import log, ceil
from embmem import EmbeddedMemory


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def echo1(
    clock,                  
    reset,

    # ---- Audio Interface ----
    au_fs,                 # sample rate strobe (data valid in)
    au_in,                 # audio input
    au_out,                # audio output    
    
    # ---- Parameters ----
    C_BD      = 8192,      # Delay Buffer depth / len   BufferLen
    C_BW      = 16,        # Delay Buffer word width    BufferWidth
    C_SR      = 48000,     # Sample Rate                SampleRate
    C_SW      = 24         # Sample width input/output  SampleWidth
    ):
    """Single channel echo

    The following is a basic single channel echo.  An input sample
    is combined with a delayed version of the sample.  This module is 
    the hardware description of the audio echo.  This description will
    be converted to Verilog/VHDL and bit-stream generated using the 
    vendor tools.

    The delay is constant and set by the C_BD parameter.  
    
    Ports
    ---------------------------------------------
      :param au_fs:  input, sample rate strobe
      :param au_in:  input, audio sample input
      :param au_out: output, audio sample output
       
    Configurable Parameters:
    ---------------------------------------------
       :param C_BD:    Delay buffer depth / len
       :param C_BW:    Delay buffer word width
       :param C_SR:    Sample rate
       :param C_SW:    Input sample bit width
       :param XDEVICE: Which Xilinx FPGA (BRAM utilization)
    """

    SampMax = 2**(C_SW-1)-1       # Max sample value
    SampMin = -1*(2**(C_SW-1)-1)  # Min sample value
    BufMax  = 2**(C_BW-1)-1       # Max buffer sample value
    BufMin  = -1*(2**(C_BW-1)-1)  # Min buffer sample value
    
    # Input registers
    _fs  = Signal(False)
    _in  = Signal(intbv(0, max=SampMax, min=SampMin))

    # Internal / Intermidiate resgisters
    _out  = Signal(intbv(0, max=SampMax, min=SampMin))    

    # Delay buffer pointers
    C_ADDR_W = int(math.log(C_BD, 2))
    wr_ptr = Signal(intbv(0, min=0, max=C_BD)) 
    rd_ptr = Signal(intbv(0, min=0, max=C_BD)) 

    # Delay Buffer Memory
    mem    = [Signal(intbv(0, max=BufMax, min=BufMin)) for i in range(C_BD)]


    #-----------------------------------------------------
    # Print some useful information about the configuration
    #-----------------------------------------------------
    totalBits  = C_BW*C_BD
    ScaleShift = int(log(2**(C_SW-C_BW), 2))
    EchoShift = 1 # the echo will be 1/2 input

    print "Delay  ............................... %f ms" % (1/float(C_SR) * C_BD * 1000)
    print "Buffer word width .................... %d" % (C_BW)
    print "Scale factor ......................... %d (%d)" % (2**(C_SW-C_BW), ScaleShift)
    print "Total Number Buffer Bits ............. %d" % (totalBits)


    for mfg,dt in EmbeddedMemory.items():
        for dev,v in dt.items():
            nblocks = ceil(float(totalBits)/v['bpb'])
            print("Number of Embedded Memory Blocks..... %d (%.2f%%)  per channel, %s.%s" % \
                      (int(nblocks),
                       (nblocks/v['total'])*100,
                       mfg, dev))


    #-----------------------------------------------------
    # HDL Description
    #-----------------------------------------------------
    @always(clock.posedge, reset.negedge)
    def hdl_desc():
        if reset == 0:
            rd_ptr.next = 0
            wr_ptr.next = 0
            _fs.next = False
            _in.next = 0
            _out.next = 0
            au_out.next = 0
        else:
            if(rd_ptr != wr_ptr) :
                rd_ptr.next = wr_ptr
            else:
                # Register the inputs
                _fs.next = au_fs
                _in.next = au_in
            
                if _fs:
                    # Scale the echo (buffered) samples
                    mem[wr_ptr].next = _in >> (ScaleShift + EchoShift)
            
                    # Update pointers to delay buffer
                    wr_ptr.next = (wr_ptr + 1) % C_BD
                    rd_ptr.next = (wr_ptr + 1) % C_BD
            
                    # Output register 1, scale back to 24 bits (shifts in hw)
                    _out.next = mem[rd_ptr] << (ScaleShift)
            
                # Output register 2, 
                au_out.next = _in + (_out)
    
        
    return hdl_desc


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
def convert():
    """Convert the RTL description to Verilog and VHDL
    """
    clock    = Signal(False)
    reset    = Signal(False)
    au_fs    = Signal(False)
    au_in    = Signal(intbv(0)[24:])
    au_out   = Signal(intbv(0)[24:])
    
    toVerilog(echo1, clock, reset, au_fs, au_in, au_out,
              C_SW=24, C_BD=2**14)

    toVHDL(echo1, clock, reset, au_fs, au_in, au_out,
           C_SW=24, C_BD=2**14)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    convert()
    

