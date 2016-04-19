
# The following is an example how to use an object to contain
# the signals for a bus.

from myhdl import *

from wishbone import Wishbone


def m_simple_top(clock, reset, buttons, leds):

    nled = len(leds)
    nbut = len(buttons)
    pouts = [Signal(False) for ii in range(nled)]
    pins = [Signal(False) for ii in range(nbut)]

    wb = Wishbone(DataWidth=8, AddressWidth=16)

    gm_ctlr = m_buttons2bus(clock, reset, wb, buttons)
    gm_gpio = [None for ii in range(len(leds))]
    for ii in range(len(leds)):
        gm_gpio[ii] = m_gpio(wb, pins[ii], pouts[ii])

    # all peripherals and controllers connected get "bus or"
    gm_bus = wb.DeviceBusses()

    @always_comb
    def rtl_assigns():
        for ii in range(nLed):
            leds.next[ii] = pouts[ii]
            pins[ii].next = buttons[ii]
    
    return gm_ctlr, gm_gpio, gm_bus, rtl_assigns


def m_gpio(wb, pin, pout, NumInputs=1, NumOutputs=1):
    """Very simple memory mapped peripheral"""

    wbdev = wb.AddDevice(Name="GPIO")
    creg = wb.AddDeviceRegister(pout, wbdev, Offset=0)
    sreg = wb.AddDeviceRegister(pin, wbdev, Offset=1, ReadOnly=True)
    ireg = wb.GetDeviceRegisters(wbdev)

    pout.assign(creg[0])
    sreg.assign(pin)

    return ireg


def m_buttons2bus(clock, reset, wb, buttons):
    """Very silly wishbone controller"""
        # states for the state-machine
    States = enum('ScanButtons', 'DoButtons', 'ReadBus',
                  'WriteBus', 'WriteBusEnd', 'End')
    state = Signal(States.ScanButtons)

    # local signals
    lbutt = Signal(intbv(0)[len(buttons):])
    devc = Signal(intbv(0, min=0, max=len(buttons)+1))
    rdat = Signal(intbv(0)[len(bb.rdat):])
    
    @always_seq(clock.posedge, reset=reset)
    def rtl():
        if state == States.ScanButtons:
            if buttons > 0:
                lbutt.next = buttons
                devc.next = 0
                state.next = States.DoButtons
                    
        elif state == States.DoButtons:
            if lbutt > 0 and lbutt[0]:
                wb.addr.next = devc
                wb.wr.next = False
                wb.rd.next = True
                state.next = States.ReadBus                
            else:
                if lbutt != buttons:
                    state.next = States.ScanButtons   

        elif state == States.ReadBus:
            wb.wr.next = False
            wb.rd.next = False

            if wb.ack:
                rdat.next = ~wb.rdat
                state.next = States.WriteBus
                
        elif state == States.WriteBus:
            if not bb.ack:
                bb.wdat.next = rdat
                bb.wr.next = True
                bb.rd.next = False
                state.next = States.WriteBusEnd
            else:
                bb.wr.next = False
                bb.rd.next = False
                
        elif state == States.WriteBusEnd:
            if bb.ack:
                state.next = States.End
            bb.wr.next = False
            bb.rd.next = False

        elif state == States.End:
            if lbutt != buttons:
                state.next = States.ScanButtons
        
    return rtl


#==============================================
    # states for the state-machine
    States = enum('ScanButtons', 'DoButtons',
                  'ReadBus', 'WriteBus', 'WriteBusEnd')
    state = Signal(States.ScanButtons)

    # local signals
    lbutt = Signal(intbv(0)[len(buttons):])
    wbutt = Signal(intbv(0)[len(buttons):])    
    devc = Signal(intbv(0, min=0, max=len(buttons)+1))
    rdat = Signal(intbv(0)[wb.DataWidth:])

    # add a new controller to the bus
    lbus = wb.AddController()
    clk,rst,cyc,stb,adr,we,sel,ack,dat_i,dat_o = wb.GetControllerSignals(lbus)
    adel = wb.AddrDelta
    
    @always_seq(clock.posedge, reset=reset)
    def rtl_silly():
        if state == States.ScanButtons:
            if buttons > 0:
                lbutt.next = buttons
                wbutt.next = buttons
                devc.next = 0
                state.next = States.DoButtons
                
        elif state == States.DoButtons:
            if lbutt > 0:
                if lbutt[0]:
                    adr.next = devc*adel
                    we.next = False
                    cyc.next = True
                    stb.next = True
                    state.next = States.ReadBus

                lbutt.next = lbutt >> 1
                devc.next = devc + 1
            else:
                # wait for the button state to change before scanning again
                if wbutt != buttons:
                    state.next = States.ScanButtons                    

        elif state == States.ReadBus:
            we.next = False
            cyc.next = False
            stb.next = False

            if ack:
                rdat.next = ~dat_i
                state.next = States.WriteBus

        elif state == States.WriteBus:
            if not ack:
                dat_o.next = rdat
                we.next = True
                cyc.next = True
                stb.next = True
                state.next = States.WriteBusEnd
            else:
                we.next = False
                cyc.next = False
                stb.next = False

        elif state == States.WriteBusEnd:
            if ack:
                state.next = States.DoButtons
            we.next = False
            cyc.next = False
            stb.next = False

        
    return rtl_silly, rtl_assigns
    
