
from myhdl import *
from stroby import stroby


def convert():
    clock = Signal(bool(0))
    reset = ResetSignal(0, active=0, async=True)
    led = Signal(intbv(0)[8:])
    
    toVerilog(stroby,clock,reset,led)
    toVHDL(stroby,clock,reset,led)

if __name__ == '__main__':
    convert()
