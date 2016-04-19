def _verify(clock, led, ClkFreq, LedRate, NumLed, NumDumb):
    cnt = 0
    numClk = int(ClkFreq*LedRate)
    Nloops = 30000
    direction = 'wait'
    ledLsb = 1
    ledMsb = 1 << len(led)

    led_last = led.val
    for ii in xrange(Nloops):
        yield clock.posedge
        cnt += 1

        if direction == 'wait':
            if (led & ledMsb) == ledMsb:
                direction = 'right'
                led_last = led.val
            elif (led & ledLsb) == ledLsb:
                direction = 'left'
                led_last = led.val
        elif led == 0:
            direction = 'wait'

        if led != led_last:
            if direction == 'right':
                assert led_last>>1 == led.val, "%x != %x" % (led, led_last)
            elif direction == 'left':
                assert led_last<<1 == led.val, "%x != %x" % (led, led_last)

            assert cnt == numClk
            cnt = 0
