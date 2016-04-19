
from __future__ import division

from math import ceil
from myhdl import *

def m_user_io(clock,reset,button,led,
              max_blink=2.,    # max blink rate in seconds
              min_blink=.033,  # min blink rate in seconds
              debounce=.1      # debounce in seconds
              ):
    """ blink the LED, button go faster
    Blink the LED at a default slow rate, each time the button
    is pressed increase the blink rate.  Once the blink rate
    reaches a maximum rate start over with the slow rate.
    The rate limits are controlled by parameters:
    *max_blink* and *min_blink* in seconds.  The button also needs
    to be debounce.  Only one rate change is desired per button
    press, to achieve this the button needs to be debounced.  The
    debounce rate is also controlled by a parameter *debounce* which
    is also in seconds.
    """

    # calculate the debounce ticks and signals
    debounce_ticks = int(round(debounce/clock.period))
    dmax = debounce_ticks*2
    print('   debounce ticks max %d'%(dmax))
    pressed_count = Signal(intbv(0,min=0,max=dmax))
    button_count = Signal(intbv(0,min=0,max=dmax))
    _button = Signal(bool(0))

    # calculate the ticks need to blink the led
    led_ticks_max = int(round(max_blink/clock.period))
    led_ticks_min = int(round(min_blink/clock.period))
    bmax,bmin = (led_ticks_max,led_ticks_min,)
    print('   blink ticks max %d min %d'%(bmax,bmin))
    blink_count_max = Signal(intbv(led_ticks_max,
                                   min=0,max=led_ticks_max*2))
    blink_count = Signal(intbv(0,min=0,max=led_ticks_max*2))


    # debounce the button, the longer the debounce the 
    # larger the counter will be
    @always_seq(clock.posedge,reset=reset)
    def rtl_debounce():
        if button == False:
            if pressed_count < debounce_ticks:
                pressed_count.next = pressed_count + 1
        else:
            if button_count >= debounce_ticks:
                _button.next = True
                button_count.next = 0
            else:
                _button.next = False

            if pressed_count > 0:
                button_count.next = pressed_count
                pressed_count.next = 0

        
    @always_seq(clock.posedge,reset=reset)
    def rtl_blink():
        if _button: # debounced button signal
            if blink_count_max > bmin:
                blink_count_max.next = blink_count_max >> 1
            else:
                blink_count_max.next = bmax
        else:
            if blink_count < blink_count_max:
                blink_count.next = blink_count + 1
            else:
                led.next = not led
                blink_count.next = 1


    return rtl_debounce, rtl_blink

