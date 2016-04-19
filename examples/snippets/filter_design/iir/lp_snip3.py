
Wp = 0.270   # end of passband, normalized frequency
Ws = 0.333   # start of the stopband frequency, normalized frequency
Rp = 0.1     # passband maximum loss (gpass)
As = 120     # stoppand min attenuation (gstop)
Filters['ellip'] = fd.iirdesign(Wp, Ws, Rp, As, ftype='ellip')
Filters['cheby2'] = fd.iirdesign(Wp, Ws, Rp, As, ftype='cheby2')
