
from myhdl import *

class BareBoneBus:
    def __init__(self):
        self.wr = Signal(False)
        self.rd = Signal(False)
        self.ack = Signal(False)
        self.rdat = Signal(intbv(0)[8:])
        self.wdat = Signal(intbv(0)[8:])
        self.addr = Signal(intbv(0)[16:])
