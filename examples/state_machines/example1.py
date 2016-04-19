
import os
import shutil
from glob import glob
import argparse

from myhdl import *

def m_think(clock,reset,thinking,sending,sent):

    states = enum('IDLE', 'THINK', 'SEND_CMD', 'ADVANCE',
                  encoding='one_hot')
    state = Signal(states.IDLE)

    # remove conversion error
    st = type(sent.val)
    lsent = Signal(st(0, min=sent.min, max=sent.max))
    sent.assign(lsent)
    
    @always_seq(clock.posedge, reset=reset)
    def rtl():
        thinking.next = False
        sending.next = False
        if state == states.IDLE:
            state.next = states.THINK
        elif state == states.THINK:
            thinking.next = True
            state.next = states.SEND_CMD
        elif state == states.SEND_CMD:
            sending.next = True
            state.next = states.ADVANCE
        elif state == states.ADVANCE:
            lsent.next = lsent+1
            state.next = states.IDLE
        else:
            assert False, "Invalid states %s"%(state)

    return rtl

def test_and_convert(args):
    clock = Signal(bool(0))
    reset = ResetSignal(0,active=0,async=True)
    thinking = Signal(bool(0))
    sending = Signal(bool(0))
    sent = Signal(intbv(0,min=0,max=10e12))

    def _test_m_think():
        asserr = Signal(bool(0))
        _t,_s,_i = [Signal(bool(0)) for _ in range(3)]
        
        tb_dut = m_think(clock,reset,thinking,sending,sent)
        
        @always(delay(3))
        def tb_clk():
            clock.next = not clock
            
        @instance
        def tb_stim():
            reset.next = reset.active
            yield delay(11)
            yield clock.posedge
            reset.next = not reset.active
            _sent = 0
            yield clock.posedge
            
            try:
                for ii in range(5):
                    _t.next,_s.next,_i.next = False,False,False
                    assert _sent == sent, "%d != %d"%(_sent,sent)
                    
                    for _ in xrange(2):
                        yield clock.posedge
                    _t.next = True
                    assert thinking
                    yield clock.posedge
                    _s.next = True
                    assert sending
                    for _ in xrange(1):
                        yield clock.posedge
                    _sent += 1
            except AssertionError, err:
                asserr.next = True
                yield delay(100)
                raise err

            raise StopSimulation
                
        return tb_dut,tb_clk,tb_stim
    
    if args.test:
        if args.trace:
            os.remove(glob('*.vcd')[0])
            g = traceSignals(_test_m_think)
        else:
            g = _test_m_think()
        Simulation(g).run()

    if args.convert:
        toVHDL(m_think,clock,reset,thinking,sending,sent)
        for vf in glob('*.vhd'):
            if os.path.isfile(os.path.join('vhd/',vf)):
                os.remove(os.path.join('vhd/',vf))
            shutil.move(vf, 'vhd/')
        
        toVerilog(m_think,clock,reset,thinking,sending,sent)
        for vf in glob('*.v'):
            if os.path.isfile(os.path.join('ver/',vf)):
                os.remove(os.path.join('ver/',vf))
            shutil.move(vf, 'ver/')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--trace',action='store_true')
    parser.add_argument('--test',action='store_true')
    parser.add_argument('--convert', action='store_true')
    args = parser.parse_args()
    test_and_convert(args)
