from random import randrange
import seven_segment
from myhdl import *
from bcd2led import bcd2led


PERIOD = 10
#def bin2str(value):
#    binstr=bin(value)[2:]
#    padding = 7-len(binstr)
#    return '0'*padding+binstr
        
def bench():
        led = Signal(intbv(0)[7:])
	bcd = Signal(intbv(0)[4:])
	clock = Signal(bool(0))
	counter= Signal(intbv(0)[7:])
	dut = bcd2led(counter, led, bcd, clock)
        

	@always(delay(PERIOD//2))
	def clkgen():
		clock.next = not clock

	@instance
	def check():
		for i in range(100):
			bcd.next = randrange(10)
			yield clock.posedge
			yield clock.negedge
			expected = int(seven_segment.encoding[int(bcd)], 2)
			assert led == expected
                        counter.next  = Signal(intbv(i)[7:])
                        print counter
		raise StopSimulation
	
	return dut, clkgen, check


def test_bench():
	tb = traceSignals(bench)
	sim = Simulation(tb)
	sim.run()
