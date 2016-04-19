
from myhdl import *

class BareBoneBus:
    
    def __init__(self):
        self.clk = Signal(False)
        self.rst = Signal(False)
        self.we = Signal(False)
        self.rd = Signal(False)
        self.data = Signal(intbv(0)[8:])
        self.addr = Signal(intbv(0)[16:])
        
    def GetControllerSignals(self):
        return (self.clk, self.rst)

    def GetDeviceSignals(self):
        return (self.clk, self.rst)
