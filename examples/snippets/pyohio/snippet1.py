
def m_button_led_wire(button,led):

    @always(button)
    def assign():
        led.next = button

    return assign
