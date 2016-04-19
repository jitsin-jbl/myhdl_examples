
import scipy
from scipy import signal
import matplotlib.pyplot
import matplotlib as mpl
import numpy as np
Fs = 2.1e6
Flow = 44e3
Fnp = Flow / (Fs/2.)
Fns = (Flow+100) / (Fs/2.)
b,a = signal.iirdesign(Fnp, Fns, 1, 40)
#b,a = signal.butter(10, Fnorm)

# ----[Plotting]----
fig = mpl.pyplot.figure()
ax = fig.add_subplot(111) 
ax.grid(True)
w,H = signal.freqz(b,a)
ax.plot(w, 20*np.log10(abs(H)))
ax.set_ylabel('Amplitude (db)', color='blue')
ax.set_xlabel('Frequency (radians)')
ay = mpl.pyplot.twinx(ax)
ay.plot(w, np.angle(H), 'r')
ay.set_ylabel(r'Phase (radians)', color='red')
