
def m_user_io(clock,reset,button,led,
              max_blink=2.,    # max blink rate in seconds
              min_blink=.033,  # min blink rate in seconds
              debounce=.1      # debounce in seconds
              ):

    # ...

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

                
