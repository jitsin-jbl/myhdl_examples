
    def taps(x, N):
        return [x] if N <= 1 else [x] + taps(Reg(x), N-1)

    w1 = sum([x*h for x,h in zip(taps(Reg(x), len(hs)), hs)])
    w2 = w1 >> len(x)/2
