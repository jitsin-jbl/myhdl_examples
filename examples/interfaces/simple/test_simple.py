
import sys
import os
from random import randint
import argparse

from myhdl import *

import wishbone
from simple import m_simple_top

def test(args):
    WaitTicks = 16
    clock = Signal(bool(0))
    reset = ResetSignal(0, active=0, async=True)
    buttons = Signal(intbv(0)[8:])
    leds = Signal(intbv(0)[8:])

    if os.path.isfile('_test.vcd'):
        os.remove('_test.vcd')

    def _test():
        tbdut = m_simple_top(clock, reset, buttons, leds)

        @always(delay(10))
        def tbclk():
            clock.next = not clock

        @instance
        def tbstim():
            print('Button to LEDs')
            reset.next = False
            yield delay(100)
            reset.next = True
            yield delay(100)
            
            for ii in range(len(buttons)):
                buttons.next[ii] = True
                for jj in range(WaitTicks):
                    yield clock.posedge
                assert leds[ii]
                buttons.next[ii] = False
                for jj in range(WaitTicks):
                    yield clock.posedge
            
            for ii in range(len(buttons)):
                buttons.next[ii] = True
                for jj in range(WaitTicks):
                    yield clock.posedge
                assert not leds[ii]
                buttons.next[ii] = False
                for jj in range(WaitTicks):
                    yield clock.posedge
            
            lleds = [False for ii in range(len(buttons))]
            for ii in [randint(0,len(buttons)-1) for qq in range(256)]:
                buttons.next[ii] = True
                lleds[ii] = not lleds[ii]
                for jj in range(WaitTicks):
                    yield clock.posedge
                assert leds[ii] == int(lleds[ii])
                buttons.next[ii] = False
                for jj in range(WaitTicks):
                    yield clock.posedge
            
            print('Success')
            raise StopSimulation
        
        return tbdut, tbclk, tbstim

    if 'trace' in args.run:
        g = traceSignals(_test)
    else:
        g = _test()
    Simulation(g).run()

    toVerilog(m_simple_top, clock, reset, buttons, leds)
    toVHDL(m_simple_top, clock, reset, buttons, leds)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('run', choices=('run', 'trace'), default='run',
                        help='simulation mode')
    args = parser.parse_args()
    test(args)

    

            

                        
