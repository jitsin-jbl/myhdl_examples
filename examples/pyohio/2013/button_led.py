
from myhdl import *

def m_button_led(clock,button,led):

    @always(clock.posedge)
    def rtl():
        led.next = button

    return rtl

def m_button_led_wire(button,led):

    @always(button)
    def assign():
        led.next = button

    return assign

