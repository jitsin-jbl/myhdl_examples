

# Stopband
Wp = [0.250, 0.350]   # Cutoff frequency 
Ws = [0.295, 0.305]   # Stop frequency 
Rp = 1                # passband maximum loss (gpass)
As = 120              # stoppand min attenuation (gstop)
Filters = {}
Filters['ellip'] = fd.iirdesign(Wp, Ws, Rp, As, ftype='ellip')
Filters['cheby2'] = fd.iirdesign(Wp, Ws, Rp, As, ftype='cheby2')
