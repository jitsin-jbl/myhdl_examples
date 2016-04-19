
import sys, os
from shutil import copyfile
import argparse

from myhdl import *
from myhdl_tools import Clock,Reset
from myhdl_tools.boards import get_xilinx_board

from stroby import *

def compile_stroby(args):
     
    brd = get_xilinx_board(args.board)
    brd.set_top(m_stroby) #CLK_FREQ,LED_RATE,NUM_DUMB
    brd.path = 'xilinx/ise/stroby_%s/'%(args.board)
    brd.convert(to='verilog')
    brd.convert(to='vhdl')
    brd.run()

    # @todo : automatically download if possible

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('board', 
                        choices=('ufo400','sx1','nexys'),
                        default='ufo400')
    args = parser.parse_args()
    compile_stroby(args)
