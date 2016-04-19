from myhdl import *

def shift_reg(clock, reset, y):

    @always_seq(clock.posedge, reset=reset)
    def rtl_shift():
        y.next = y << 1

    return rtl_shift

def TestBench():

    clock = Signal(bool(0))
    reset = ResetSignal(0, active=1, async=False)
    y = Signal(intbv(1)[4:])

    tb_dut = traceSignals(shift_reg, clock, reset, y)
    
    @always(delay(1))
    def tb_clkgen():
        clock.next = not clock

    @instance
    def tb_stim():
        reset.next = True
        yield delay(2)
        reset.next = False

        for ii in xrange(4):
            yield clock.negedge
            print("%3d  %s" % (now(), bin(y, 4)))

        raise StopSimulation

    return tb_dut, tb_clkgen, tb_stim

if __name__ == '__main__':
    Simulation(TestBench()).run()
                  
    
