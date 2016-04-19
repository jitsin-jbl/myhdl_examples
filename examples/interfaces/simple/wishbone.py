
from myhdl import *

class WishboneDeviceRegister():
    def __init__(self, rio, lreg, Offset, ReadOnly, Name=""):
        self.rio = rio
        self.lreg = lreg
        self.Offset = Offset
        self.ReadOnly = ReadOnly
        self.Name = Name

    def AddDescription(self, desc):
        """Add registers description/documentation"""
        self.desc = desc

    def AddBits(self, bitName, bit):
        """Add a short-cut to the bit"""
        assert isinstance(bitName, str)
        if not self.__dict__.has_key(bitName):
            self.__dict__[bitName] = bit
            #self.bits.append
    
class WishboneDevice():
    def __init__(self, dat_o, ack, BaseAddr=0, Name=""):
        self.BaseAddr = BaseAddr
        self.dat_o = dat_o
        self.ack = ack
        self.registers = []
        self.name = Name

class WishboneController():
    def __init__(self, Name=""):
        self.name = Name
        
class Wishbone():

    def __init__(self, DataWidth=8, AddressWidth=16):
        self.DataWidth = DataWidth
        self.AddressWidth = AddressWidth
        self.clk = Signal(False)
        self.rst = Signal(False)
        self.cyc = Signal(False)
        self.stb = Signal(False)
        self.adr = Signal(intbv(0)[AddressWidth:])
        self.we = Signal(False)
        self.sel = Signal(intbv(0)[int(DataWidth/8)])
        self.ack = Signal(False)
        
        # The data buses are a slightly special case.  The
        # dat_o is broadcast to a the device (peripherals) 
        # and dat_i is an or of all the device buses.  This 
        # class will have a generator that will or all the buses
        # together.
        self.dat_i = Signal(intbv(0)[DataWidth:])
        self.dat_o = Signal(intbv(0)[DataWidth:])
        self.devices = []
        self.AddrDelta = 0x100

        # @todo: should do the same thing for multiple controllers,
        #        currently only 1 controller supported.

    
    def DeviceBusses(self):
        """
        After all devices/peripherals have been added this function should
        be called to get the generator that 'or's together all the device
        busses.
        """
        nDevs = len(self.devices)
        clk = self.clk
        dat_i = self.dat_i
        ack = self.ack
        dev_acks = [self.devices[ii].ack for ii in range(nDevs)]
        dev_dats = [self.devices[ii].dat_o for ii in range(nDevs)]

        # At this point all the addresses could be "optimized" 

        @always_comb
        def rtl_or_combine():
            dats = 0
            acks = 0
            for ii in range(nDevs):
                dats = dats | dev_dats[ii]
                acks = acks | dev_acks[ii]

            dat_i.next = dats
            ack.next = acks

                         
        def los_monitor(dev_dats, dev_acks):
            ack0,ack1,ack2,ack3,ack4,ack5,ack6,ack7 = [Signal(False) for ii in range(8)]
            dat0,dat1,dat2,dat3,dat4,dat5,dat6,dat7 = [Signal(intbv(0)[8:]) for ii in range(8)]
        
            @always_comb
            def rtl_debug_monitor():
                ack0.next = dev_acks[0]
                ack1.next = dev_acks[1]
                ack2.next = dev_acks[2]
                ack3.next = dev_acks[3]
                ack4.next = dev_acks[4]
                ack5.next = dev_acks[5]
                ack6.next = dev_acks[6]
                ack7.next = dev_acks[7]
                
                dat0.next = dev_dats[0]
                dat1.next = dev_dats[1]
                dat2.next = dev_dats[2]
                dat3.next = dev_dats[3]
                dat4.next = dev_dats[4]
                dat5.next = dev_dats[5]
                dat6.next = dev_dats[6]
                dat7.next = dev_dats[7]

            return  rtl_debug_monitor

        mon = [los_monitor(dev_dats, dev_acks)] if False else []
        return [rtl_or_combine] + mon


    def AddDevice(self, BaseAddress=None, Name=""):
        nextBus = Signal(intbv(0)[self.DataWidth:])
        nextAck = Signal(False)
        
        if BaseAddress is not None:
            nextAdr = BaseAddress
        else:
            if len(self.devices) > 0:
                nextAdr = self.AddrDelta+self.devices[-1].BaseAddr
            else:
                nextAdr = 0
                
        wbdev = WishboneDevice(nextBus, nextAck, nextAdr, Name)
        self.devices.append(wbdev)
        
        return wbdev

    
    def AddDeviceRegister(self, rio, wbdev, Offset=0, ReadOnly=False, Name=""):
        
        # @todo : calculate offset
        lreg = Signal(intbv(0)[len(rio):])
        wbreg = WishboneDeviceRegister(rio, lreg, Offset, ReadOnly, Name) 
            
        wbdev.registers.append(wbreg)

        return lreg

    def GetDeviceRegisters(self, wbdev):
        """Return the generators for the registers """

        # short cuts
        clk,rst,cyc,stb,adr,we,
        sel,ack,dat_i,dat_o = (self.clk,self.rst,self.cyc,self.stb,
                               self.adr,self.we,self.sel,wbdev.ack,
                               self.dat_o,wbdev.dat_o)

        nRegs = len(wbdev.registers)
        selected = Signal(False)
        offset = Signal(intbv(0, min=0, max=nRegs))
        BaseAddr = wbdev.BaseAddr
        MaxOffset = max([wbdev.registers[ii].Offset for ii in range(nRegs)])
        lregs = [wbdev.registers[ii].lreg for ii in range(nRegs)]
        ro = ''
        for ii in range(nRegs-1,-1,-1):
            ro += str(int(wbdev.registers[ii].ReadOnly))
        ReadOnly = Signal(intbv(ro, min=0, max=2**nRegs))
        @always_comb
        def rtl_decode():
            if cyc and stb and (adr >= BaseAddr and adr <= BaseAddr+MaxOffset):
                selected.next = True
                offset.next = adr - BaseAddr
            else:
                selected.next = False
                offset.next = 0

        @always(clk.posedge)
        def rtl_wb_register():
            if not rst:
                dat_o.next = 0
                for ii in range(nRegs):
                    lregs[ii].next = 0
            else:
                if selected:
                    ack.next = True
                    if we:
                        if not int(ReadOnly[offset]):
                            #print(offset, dat_i[len(lregs[offset]):])
                            #print(lregs)
                            lregs[offset].next = dat_i[len(lregs[offset]):]
                        dat_o.next = 0
                    else:
                        dat_o.next = lregs[offset]
                else:
                    dat_o.next = 0
                    ack.next = False
            
            
        return rtl_decode, rtl_wb_register
    
    def GetDeviceSignals(self, wbdev):
        return (self.clk, self.rst, self.cyc, self.stb,
                self.adr, self.we, self.sel, self.ack, self.dat_i, wbdev.dat_o)

    def AddController(self):
        pass

    def GetControllerSignals(self, wbctlr=None):
        return (self.clk, self.rst, self.cyc, self.stb,
                self.adr, self.we, self.sel, self.ack, self.dat_i, self.dat_o)

    def Summary(self):
        """ Create a string with the summary of the configured bus"""
        summary = ""
        for dev in self.devices:
            summary += "%s @ address 0x%04X\n" % (dev.name, dev.BaseAddr)
            for reg in dev.registers:
                summary += "  registers %s @ offset %d\n" % (reg.name, reg.offset)

        return summary
