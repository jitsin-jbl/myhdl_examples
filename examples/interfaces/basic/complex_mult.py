
from myhdl import *

class C(object): pass

def complex_mult(clock, reset, a, b, c):

    a_real,a_imag = a.real,a.imag
    b_real,b_imag = b.real,b.imag
    c_real,c_imag = c.real,c.imag

    @always_seq(clock.posedge, reset=reset)
    def hdl_mult():
        c_real.next = (a_real * b_real) - (a_imag * b_imag)
	c_imag.next = (a_real * b_imag) + (a_imag * b_real)

    return hdl_mult


def complex_top(clock, reset, a_real, a_imag, b_real, b_imag, c_real, c_imag):

    a,b,c = C(),C(),C()
    a.real = a_real
    a.imag = a_imag
    b.real = b_real
    b.imag = b_imag
    c.real = c_real
    c.imag = c_imag	
    
    g_cm = complex_mult(clock, reset, a, b, c)

    return g_cm

def test():

    clock = Signal(False)
    reset = ResetSignal(False, active=0, async=True)
    a_real = Signal(intbv(0, min=-8, max=8))	
    a_imag = Signal(intbv(0, min=-8, max=8))		
    b_real = Signal(intbv(0, min=-8, max=8))	
    b_imag = Signal(intbv(0, min=-8, max=8))		
    c_real = Signal(intbv(0, min=-128, max=129))	
    c_imag = Signal(intbv(0, min=-128, max=129))		
        
    def _test():
        tb_dut = complex_top(clock, reset, a_real, a_imag, 
                             b_real, b_imag, c_real, c_imag)
        @always(delay(2))
	def tb_clkgen():
	    clock.next = not clock

	@instance
	def tb_stimulus():
            reset.next = False
	    yield delay(12)
	    reset.next = True
	    yield delay(12)

	    for ar in range(-8,8):
                for ai in range(-8,8):
                    for br in range(-8, 8):
                        for bi in range(-8, 8):
                            a_real.next = ar
			    a_imag.next = ai
			    b_real.next = br
			    b_imag.next = bi
                            a = ar + ai*1j
			    b = br + bi*1j
			    c = a * b
			    yield clock.posedge
			    yield clock.posedge
			    assert c.real == c_real, "r %d != %d" % (c.real, c_real)
			    assert c.imag == c_imag, "i %d != %d" % (c.imag, c_imag)
			    
	    raise StopSimulation

        return tb_dut, tb_clkgen, tb_stimulus

    Simulation(traceSignals(_test)).run()
    toVerilog(complex_top, clock, reset, a_real, a_imag, b_real, b_imag, c_real, c_imag)

    
if __name__ == '__main__':
    test()
