from myhdl import *

# range for the intbv used
min,max = (-8,8)

# example singals to the m_nice_logic ports
clock = Signal(bool(0))
a,b = [Signal(intbv(0, min=min, max=max))
       for _ in range(2)]
mode = Signal(bool(0))
q2,q3 = [Signal(intbv(0, min=3*min, max=3*max))
         for _ in range(2)]

def m_nice_logic(clock, a, b, mode, q2, q3):
    q1 = intbv(0, min=q2.min, max=q2.max)
    
    @always(clock.posedge)
    def rtl():
        if mode:
            q1[:] = a + b
        else:
            q1[:] = a - b
            
        # note the comment doesn't match the code
        # on the page, dividing a value makes it smaller
        #print("q1 %d, q2 %d"%(q1,q2))
        q2.next = q1 + (q2 >> 2)

    @always(clock.posedge)
    def rtl_piped():
        q3.next = q1 + (q2 >> 2)

    return rtl, rtl_piped


def test():

    tb_dut = m_nice_logic(clock, a, b, mode, q2, q3)

    #tb_clk = clock.gen()
    @instance
    def tb_clk():
        clock.next = 0
        while True:
            yield delay(3)
            clock.next = not clock
    
    @instance
    def tb_stim():
        for mm in range(2):
            mode.next = bool(mm)
            for aa in range(min,max):
                for bb in range(min,max):
                    a.next = aa
                    b.next = bb
                    yield clock.posedge
                    
                    for ii in range(5):
                        yield clock.posedge
                        assert q3 == q2
                        
        raise StopSimulation

    return tb_dut, tb_clk, tb_stim

        
if __name__ == '__main__':
    Simulation(traceSignals(test)).run()
    toVerilog(test)
    toVHDL(test)


