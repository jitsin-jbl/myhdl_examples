

if strobe:
    if led_bit_mem[MSB]:
        led_bit_mem.next = (1 << MB-2)
        left_not_right.next = False
    elif led_bit_mem[LSB]:
        led_bit_mem.next = 2
        left_not_right.next = True
    else:
        if left_not_right:
            led_bit_mem.next = led_bit_mem << 1
        else:
            led_bit_mem.next = led_bit_mem >> 1
