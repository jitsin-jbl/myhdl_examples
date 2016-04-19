
def mm_median(sys, wi, wo, med):    
    N,st = len(wi), wi[0]
    z = [wi,] + [[Signal(st.val) for _ in range(N)]
                      for stage in range(N-1)] + [wo,]

    gcmp = [m_cmp(sys, z[ii], z[ii+1], ii) 
            for ii in range(N)]
    
    MN = N//2
    @always_comb 
    def rtlmed():
        med.next = wo[MN]

    return gcmp, rtlmed
