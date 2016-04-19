import shutil
import numpy
from scipy.io import loadmat
from siir import SIIR
from myhdl import Simulation

matfile = loadmat('sos.mat')  
sos = matfile['sos']

# Create the sections manually
b = numpy.zeros((3,3))
a = numpy.zeros((3,3))
section = [None for ii in range(3)]
for ii in xrange(3):
    b[ii] = sos[ii,0:3]
    a[ii] = sos[ii,3:6]

    section[ii] = SIIR(b=b[ii], a=a[ii], W=(24,0))
    section[ii].Convert()  # Create the Verilog for the section
    shutil.copyfile('siir_hdl.v', 'iir_sos_section%d.v'%(ii))
    #dut = section[ii].TestFreqResponse()
    #Simulation(dut).run()
    #section[ii].PlotResponse(fn='iir_sos_section%d.png'%(ii))

# Create a single module
iir_sos = SIIR(sos=sos, W=(24,0))
iir_sos.Convert()
dut = iir_sos.TestFreqResponse()
Simulation(dut).run()
iir_sos.PlotResponse(fn='iir_sos')

