

from numpy import *
from scipy import signal
from scipy.signal import filter_design as fd
from matplotlib import pyplot as plt

# Specification for our filter
Wp = 0.412   # Cutoff frequency 
Ws = 0.270   # Stop frequency 
Rp = 0.1     # passband maximum loss (gpass)
As = 60      # stoppand min attenuation (gstop)

Filters = {'ellip' : (), 'cheby2' : (), 'butter' : (), 'cheby1' : (),  'bessel' : ()}

# ellip and cheby2 filter design
Filters['ellip'] = fd.iirdesign(Wp, Ws, Rp, As, ftype='ellip')
Filters['cheby2'] = fd.iirdesign(Wp, Ws, Rp, As, ftype='cheby2')

# The butter and cheby1 need less constraint spec
Rpl = Rp*10; Asl = As/4.
Filters['butter'] = fd.iirdesign(Wp, Ws, Rp, As, ftype='butter')
Filters['cheby1'] = fd.iirdesign(Wp, Ws, Rp, As, ftype='cheby1')

# The bessel max order of 8 for this cutoff, can't use
# iirdesign have to use iirfilter.
Filters['bessel'] = fd.iirfilter(8, Wp, btype='highpass', ftype='bessel')


