
from myhdl import *
from mysig import Clock,Reset

def m_clk_io_gen(clock,reset,clk_io,clk_io_posedge,clk_io_freq=100e3):
    """ generate an slow (very slow) clock for serail comms """
    
    Nticks = int(clock.frequency/clk_io_freq/2)
    cnt = Signal(intbv(1,min=0,max=Nticks+1))
    
    @always_seq(clock.posedge,reset=reset)
    def hdl():
        if cnt == Nticks:
            cnt.next = 1
            clk_io.next = not clk_io
            if not clk_io:
                clk_io_posedge.next = True
        else:
            cnt.next = cnt + 1
            clk_io_posedge.next = False
            
    return hdl


def test_clk_io_gen():
    clk_io_freq = 100e3
    clock = Clock(0,frequency=100e6)
    reset = Reset(0,active=0,async=True)
    clk_io = Signal(bool(0))
    clk_io_posedge = Signal(bool(0))
    
    tb_dut = traceSignals(m_clk_io_gen,clock,reset,
                          clk_io,clk_io_posedge,
                          clk_io_freq=clk_io_freq)
    tb_clk = clock.gen(hticks=5)
    
    @instance
    def tb_stim():
        yield reset.pulse(23)
        for ii in xrange(10):
            yield clk_io.posedge
        raise StopSimulation
    
    Simulation((tb_dut,tb_clk,tb_stim)).run()
    toVerilog(m_clk_io_gen,clock,reset,
              clk_io,clk_io_posedge,
              clk_io_freq=clk_io_freq)

    toVHDL(m_clk_io_gen,clock,reset,
           clk_io,clk_io_posedge,
           clk_io_freq=clk_io_freq)


if __name__ == '__main__':
    test_clk_io_gen()
