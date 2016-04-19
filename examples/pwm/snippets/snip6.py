

R = np.array([9,10,10,10])
Rt = np.array([9,9*10,9*100,9*1000])
Fss = Fs/Rt

Fns = Fs
yf = yn.copy()
for rr,ff in zip(R,Fss):
    Fp = Fns
    Wp = (Fp-.1*Fp)/(Fns/2)
    Ws = Fp/(Fns/2)
    Rp = .3
    As = 80
    b,a signal.filter_design.iirdesign(Wp,Ws,Rp,As,ftype='ellip')
    Fns = Fns/rr
    yf = yf[::rr]  # filtered, reduce the numbrer of samples
