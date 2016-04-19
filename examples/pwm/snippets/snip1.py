
# Create a 1st order butterworth filter
Fs = 288e6
Fpwm = 32e3
b,a = signal.butter(1, (Fpwm/2)/(Fs/2))


