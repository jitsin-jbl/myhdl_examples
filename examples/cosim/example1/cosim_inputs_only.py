
import os
import sys
import argparse
import traceback

from myhdl import *
from mysig import Clock,Reset

def cosim_icarus(func, **ports):
    assert os.path.isfile('./myhdl.vpi'), \
           "missing myhdl.vpi file, copy or link here '.'"
    fn = func.func_name
    cmd = 'iverilog -o %s %s.v tb_%s.v'%(fn,fn,fn)
    print(cmd)
    os.system(cmd)
    cmd = 'vvp -m ./myhdl.vpi %s'%(fn)
    print(cmd)
    return Cosimulation(cmd, **ports)

def m_inputs_only(clock,reset):
    v = Signal(modbv(0)[3:])
    
    @always(clock.posedge)
    def hdl():
        vv = 0
        if not reset:
            vv = v + 1
        v.next = vv

    return hdl

def m_inputs_outputs(clock,reset,v):

    @always(clock.posedge)
    def hdl():
        vv = 0
        if not reset:
            vv = v + 1
        v.next = vv

    return hdl    
    
def test(tb_dut,clock,reset,v):
    tb_clk = clock.gen()
    @instance
    def tb_stim():
        yield reset.pulse(10)
        while now() < 23:
            yield clock.posedge
            print(v)
        raise StopSimulation

    Simulation((tb_dut,tb_clk,tb_stim)).run()

def run_test(f='i'):
    assert f in ('i','o'), "Incorrect option, must be 'i' or 'o'"
    msg = {'i':'inputs','o':'inputs and outputs'}
    clock,reset = (Clock(0), Reset(0,active=1,async=False))
    v = Signal(modbv(0)[3:])
    print('%s'%f+'-'*48)
    if f == 'i':
        toVerilog(m_inputs_only,clock,reset)
        tb_dut = cosim_icarus(m_inputs_only,clock=clock,reset=reset)
    else:
        toVerilog(m_inputs_outputs,clock,reset,v)
        tb_dut = cosim_icarus(m_inputs_outputs,clock=clock,reset=reset,v=v)

    try:
        test(tb_dut,clock,reset,v)
    except:
        print('%s cosimulation failed'%(msg[f]))
        traceback.print_exc()
    del(tb_dut)
    print('%s'%f+'-'*48)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test a cosim config')
    parser.add_argument('f', type=str, choices=('i','o'),
                        help='test inputs only (i) or inputs and outputs (o) to cosim')
    args = parser.parse_args()
    run_test(args.f)
