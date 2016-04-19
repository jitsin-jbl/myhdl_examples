
# Bandpass
Wp = [0.270, 0.333]   # Cutoff frequency 
Ws = [0.230, 0.373]   # Stop frequency 
Rp = 0.1              # passband maximum loss (gpass)
As = 110              # stoppand min attenuation (gstop)
Filters = {}
Filters['ellip'] = fd.iirdesign(Wp, Ws, Rp, As, ftype='ellip')
Filters['cheby2'] = fd.iirdesign(Wp, Ws, Rp, As, ftype='cheby2')