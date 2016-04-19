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
The following is an example using the modbv type available in
MyHDL 0.8.
"""

from myhdl import *
from math import log, ceil
from random import randint
import time

def example_modbv(clk, rst, x, y,
                  D   = 16,
                  Max = 127,
                  Min = -1*127
                  ):
    """Recursive windowed (moving) averager

    The following is an implementation of a recursive windowed average (RWA).
    Sometimes call a recursive running sum, if the value is not scaled at the
    end.  The difference equation for the RWA :

        y[n] = y[n-1] + x[n] - x[n-D]

    The actual implementation arranges the above difference equation so that
    the accumulator is first.  The accumulator has a \"pole\" at zero frequency,
    ( for low frequency signals the gain is high accumulator will overflow,
      infinite at 0 rad/sec).
      
    The differ has a zero that cancels out the pole, the null will unwrap the
    accumulator.  Both the accumulator and differ terms will wrap.

    Note : The first implementation of the module below the term (x + acc) was
           used in many spots.  In this case, aach of the Signal types would
           have needed to be a modbv.  I wanted to show the mixing of types,
           so instead of using the common (x + acc) in many of the assignments,
           an intermediate signal was used.           
    """

    # The windowed average has a gain equal to the length of the window.
    # The recursive versions is has the same gain.
    Max = D*Max
    Min = D*Min
    lD  = int(log(D,2))
    
    delay = [Signal(intbv(0, min=Min, max=Max)) for ii in range(D)]
    isum  = Signal(modbv(0, min=Min, max=Max))
    acc   = Signal(intbv(0, min=Min, max=Max))
    diff  = Signal(modbv(0, min=Min, max=Max))
    cnt   = Signal(modbv(0, min=0, max=D))


    @always_comb
    def rtl_sum_diff():
        isum.next = (x + acc)
                
    @always(clk.posedge)
    def rtl_accum_delay():
        if rst:
            acc.next  = 0
            cnt.next  = 0
        else:            
            # Accumulator (infinite gain at DC)
            acc.next = isum

            # delay buffer
            delay[cnt].next = isum
            cnt.next = cnt + 1

    @always_comb
    def rtl_diff():
        diff.next = isum - delay[cnt]

    # zero clock delay output, actual implementations might want
    # register the outputs
    @always_comb
    def rtl_out():
        # accumulator and diff
        y.next = diff >> lD


    return rtl_sum_diff, rtl_accum_delay, rtl_diff, rtl_out
