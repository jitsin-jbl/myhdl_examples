# Copyright (c) 2011-2013 Christopher Felton
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
import os
import random
from copy import copy
import argparse

from myhdl import *

from stroby import *

class DutObj():
    """
    object wrapper around the design under test.
    """
    def __init__(self, ClkFreq=100, LedRate=0.3, NumLed=8, NumDumb=4):
        self.clock = Signal(False)
        self.reset = ResetSignal(0, active=0, async=True)
        self.leds = Signal(intbv(0)[NumLed:])
        self.ClkFreq = ClkFreq
        self.LedRate = LedRate
        self.NumLed = NumLed
        self.NumDumb = NumDumb

    def Gens(self, TraceSignals=False):

        if TraceSignals:
            dut = traceSignals(m_stroby,
                               self.clock, self.reset, self.leds,
                               CLK_FREQ=self.ClkFreq,
                               LED_RATE=self.LedRate,
                               NUM_DUMB=self.NumDumb)
        else:
            dut = m_stroby(
                self.clock, self.reset, self.leds,
                CLK_FREQ=self.ClkFreq,
                LED_RATE=self.LedRate,
                NUM_DUMB=self.NumDumb)        

        @always(delay(2))
        def tb_clkgen():
            self.clock.next = not self.clock

        return  dut, tb_clkgen

def _verify(clk, led, ClkFreq, LedRate, NumLed, NumDumb):
    cnt = 0
    numClk = int(ClkFreq*LedRate)
    NumStrobes = 33
    MaxTicks = 3*numClk*2*NumDumb
    direction = 'wait'
    ledLsb = 1
    ledMsb = 1 << len(led)-1

    led_last = copy(led.val)
    while NumStrobes > 0:
        yield clk.posedge
        cnt += 1

        if direction == 'wait':
            if (led & ledMsb) == ledMsb:
                direction = 'right'
                led_last = copy(led.val)
                cnt = 0
            elif (led & ledLsb) == ledLsb:
                direction = 'left'
                led_last = copy(led.val)
                cnt = 0
        elif led == 0:
            direction = 'wait'
            led_last = 0

        if led != led_last:
            if direction == 'right':
                assert led_last>>1 == led.val, "%x != %x" % (led, led_last)
            elif direction == 'left':
                assert led_last<<1 == led.val, "%x != %x" % (led, led_last)

            assertMsg = 'cnt %d, numClk %d, %0x(%0x) %s' % \
                (cnt, numClk, led, led_last, direction)
            assert cnt == numClk, assertMsg
            cnt = 0
            NumStrobes -= 1
            led_last = copy(led.val)

        assert cnt < MaxTicks, "Too many ticks and no LED strobe"
    
def test_random():
    
    @instance
    def tb_stimulus():
        i.reset.next = False
        yield delay(100)
        i.reset.next = True

        yield _verify(i.clock, i.leds, ClkFreq, LedRate, NumLed, NumDumb)

        raise StopSimulation

    ClkFreq = random.randint(20, 5000)
    LedRate = 0
    while LedRate < .2: LedRate = random.random()
    NumLed  = random.randint(2,64)
    NumDumb = random.randint(1,16)
    i = DutObj(ClkFreq=ClkFreq, LedRate=LedRate, 
               NumLed=NumLed, NumDumb=NumDumb)
    dut = i.Gens(TraceSignals=True)    
    print('  sim clock freq %d led rate %.3f num led %d num dumb (holders) %d ' % \
              (ClkFreq, LedRate, NumLed, NumDumb))
    sim = Simulation((dut, tb_stimulus))
    sim.run()

def _create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', type=int, default=3,
                        help='number of loops to test')
    return parser

if __name__ == '__main__':
    parser = _create_parser()
    args = parser.parse_args()
    for ii in xrange(args.N):
        test_random()
