The following are some simple instructions on how to use the the IIR HDL
generator.  More inforation can be found at 
`here <http://www.fpgarelated.com/showarticle/7.php>`_ and 
`here <http://www.dsprelated.com/showcode/211.php>`_.

::
	
   # Instantiate the SIIR object.  Pass the cutoff frequency
   # Fc and the sample rate Fs in Hz.  Also define the input
   # and output fixed-point type.  W=(wl, iwl) where
   # wl = word-length and iwl = integer word-length.  This
   # example uses 23 fraction bits and 1 sign bit.
   >>> from siir import SIIR
   >>> flt = SIIR(Fstop=1333, Fs=48000, W=(24,0))
   
   # Plot the response of the fixed-point coefficients
   >>> plot(flt.hz, 20*log10(flt.h)
   
   # Create a testbench and run a simulation
   # (get the simulated response)
   >>> from myhdl import Simulation
   >>> tb = flt.TestFreqResponse(Nloops=128, Nfft=1024)
   >>> Simulation(tb).run()
   >>> flt.PlotResponse()
   
   # Happy with results generate the Verilog and VHDL
   >>> flt.Convert()

