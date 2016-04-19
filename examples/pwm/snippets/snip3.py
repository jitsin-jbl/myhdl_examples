
Wp = 15e3/(Fs/2.)
Ws = 30e3/(Fs/2.)
Rp = .1
As = 20.
b,a = signal.filter_design.iirdesign(Wp,Ws,Rp,As,ftype='ellip')
w,H = signal.freqz(b,a)  # filter response
