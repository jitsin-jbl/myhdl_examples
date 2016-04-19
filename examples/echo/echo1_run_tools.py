# Copyright (c) 2011,2012 Christopher Felton
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import sys, os
from shutil import copyfile
from myhdl import *
from stroby import *

from tools import *

def _downloadEcho(brd, bit_file):
    """ Download bit file to a board supported by the USBP framework.
    This has been successfully used with the SX1 and UFO400 boards.  It 
    should be possible to use USBP to download the nexsys unmodified.  To
    download the DE2 modificaitons would be required to the USBP framework.
    """
    if brd == 'sx1':
        brd = 'sx'

    print('Download bit-file, %s,  to development board %s' %(brd, cfile))
    try:
        import usbp
        usb = usbp.USBP(brd)
        usb.ConfigFpga(bit_file)
    except:
        print "Failed to program board"

def _createSx1Fpga(ppath):
    """Run the Xilinx tools
    """    
    # set up pin configuration for the FPGA
    fpga = Fpga(path=ppath)
    fpga.setPin('reset', 'P13')
    fpga.setPin('clk', 'P35')
    fpga.setPin('led[0]', 'P90')
    fpga.setPin('led[1]', 'P91')
    fpga.setPin('led[2]', 'P92')
    fpga.setPin('led[3]', 'P94')
    fpga.setPin('led[4]', 'P95')
    fpga.setPin('led[5]', 'P96')
    fpga.setPin('led[6]', 'P99')
    fpga.setPin('audio_clk', 'P63')
    fpga.setPin('audio_bclk', 'P85')
    fpga.setPin('audio_din', 'P62')
    fpga.setPin('audio_lrcin', 'P65')
    fpga.setPin('audio_lrcout', 'P68')
    fpga.setPin('audio_csn', 'P84')
    fpga.setPin('audio_sclk', 'P78')
    fpga.setPin('audio_sdin', 'P79')
    fpga.setPin('audio_mode', 'P66')
    fpga.setPin('audio_dout', 'P69')
    fpga.setDevice('spartan3e', 'xc3s500e', 'vq100', '-5')
    return fpga

def _runTools(fpga, ppath, vfile):
    imp = Xilinx(ppath, 'echo1')
    imp.setFpga(fpga)
    imp.addHdl((vfile))
    imp.createTcl()
    imp.run()

def ConvertRunProg(brd='sx1'):
    """Convert the design, run it through the tools (if available), and download
    """

    SupportedBoards = ['sx1']
    if brd not in SupportedBoards:
        print('Board must be one of the following:')
        print('%s' % (str(SupportedBoards)))
        return
    else:
        print('Converting MyHDL to Verilog for board %s' % (brd))
    
    clk = Signal(False)
    au_fs = Signal(False)
    au_in = Signal(False)
    au_out = Signal(False)

    if brd == 'sx1':
        # Create a Verilog for the DSPtronics Signa-X1
        toVerilog(echo1, clk, au_fs, au_in, au_out)
        ppath = 'ise_xilinx/echo_sx1/'
        vfile = 'sx1_echo1.v'
        copyfile('echo1.v', ppath+vfile)
        fpga = _createSx1Fpga(ppath)
        _runTools(fpga, ppath, vfile)
    
    else:
        print('Incorrect board %s' % (brd))


if __name__ == '__main__':
    ConvertRunProg(sys.argv[1])

