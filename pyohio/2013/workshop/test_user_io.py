
import argparse
from argparse import Namespace

from myhdl import *
from myhdl_tools import Clock,Reset

from user_io import m_user_io

def test_user_io(args):
    clock = Clock(0,frequency=1e3)
    reset = Reset(0,active=0,async=False)
    button = Signal(bool(1))
    led = Signal(bool(0))

    def _test_user_io():
        
        tb_dut = m_user_io(clock,reset,button,led)
        tb_clk = clock.gen()
        
        @instance
        def tb_stim():
            yield reset.pulse(100)
            
            for bb in xrange(10):
                button.next = False
                yield delay(400*6)
                button.next = True
                yield delay(100)
            
                for ii in xrange(1000):
                    yield delay(100)

            raise StopSimulation

        return tb_dut,tb_clk,tb_stim

    Simulation(traceSignals(_test_user_io)).run()

if __name__ == '__main__':
    args = Namespace()
    test_user_io(args)
