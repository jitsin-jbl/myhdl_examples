from myhdl import *

def m_buttons(clock, reset, bb, buttons):
    """Very silly bare bus controller
    
    This will generate a bus cycle when a discrete 
    button is pushed.
    """
    
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
                bb.addr.next = devc
                bb.wr.next = False
                bb.rd.next = True
                state.next = States.ReadBus                
            else:
                if lbutt != buttons:
                    state.next = States.ScanButtons   

        elif state == States.ReadBus:
            bb.wr.next = False
            bb.rd.next = False

            if bb.ack:
                rdat.next = ~bb.rdat
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
