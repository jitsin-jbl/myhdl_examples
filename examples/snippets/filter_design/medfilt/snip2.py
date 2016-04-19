
def median(x):
    N = len(x)
    def compare_stage(z, stage, N):
        t,k = copy(z), 0 if (stage%2) else 1        
        for ii in range(k,N-1, 2):
            t[ii] = min(z[ii], z[ii+1])
            t[ii+1] = max(z[ii], z[ii+1])
        return t

    z = x
    for stage in range(N):
        z = compare_stage(z, stage, N)

    return z[N//2], z