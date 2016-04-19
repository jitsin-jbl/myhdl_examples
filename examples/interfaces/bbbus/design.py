

from myhdl import *

from bbbus import BareBoneBus
from button import m_buttons

def m_design_top(clock, reset, btn, led):
    """ interfaces example top-level
    """
    bb = BareBoneBus()

    gb = m_buttons(clock, reset, bb, btn)
    gl = m_leds(clock, reset, bb, led)

    return gb, gl


def m_leds(clock, reset, bb, leds):
    """ bus cycle to LEDs
    """

    lled = Signal(intbv(0)[len(leds):])

    @always_seq(clock.posedge, reset=reset)
    def rtl():
        if bb.rd and bb.addr == 0:
            bb.rdat.next = lled
            bb.ack.next = True
            
        elif bb.wr and bb.addr == 0:
            lled.next = bb.wdat
            bb.ack.next = True

        else:
            bb.ack.next = False

        leds.next = lled


    return rtl

