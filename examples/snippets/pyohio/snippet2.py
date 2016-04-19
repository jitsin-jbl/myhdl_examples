
def m_button_led(clock,button,led):

    @always(clock.posedge)
    def rtl():
        led.next = button

    return rtl
