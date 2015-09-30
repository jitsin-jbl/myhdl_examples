from random import randrange
from flipflop import *
def test_latch():

    q, d, g = [Signal(bool(0)) for i in range(3)]

    latch_inst = latch(q, d, g)

    @always(delay(7))
    def dgen():
        d.next = randrange(2)

    @always(delay(41))
    def ggen():
        g.next = randrange(2)


    return latch_inst, dgen, ggen

def simulate(timesteps):
    tb = traceSignals(test_latch)
    sim = Simulation(tb)
    sim.run(timesteps)

simulate(20000)

def convert():
    q, d, g  = [Signal(bool(0)) for i in range(3)]
    toVerilog(latch, q, d, g)

convert()
