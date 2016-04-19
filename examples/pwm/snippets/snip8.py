


   @always_seq(clock.posedge, reset=reset)
    def hdl_pwm():
        if tcnt == Tmax-1:
            tcnt.next = 0
            ts.next = True
            y.next = 1
        else:
            tcnt.next = tcnt + 1
            ts.next = False
            if tcnt >= xu:
                y.next = 0
