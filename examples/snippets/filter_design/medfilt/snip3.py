
def m_cmp(sys, x, z, stage=0):
    N,K = len(z), 0 if stage%2 else 1
    B = 0 if K == 1 else N-1
    @always_seq(sys.clock.posedge, reset=sys.reset)
    def rtl():
        z[B].next = x[B] # pass-thru
        for ii in range(K, N-1, 2):
            z[ii].next   = x[ii] if x[ii] < x[ii+1] else x[ii+1] 
            z[ii+1].next = x[ii] if x[ii] > x[ii+1] else x[ii+1] 

    return rtl
