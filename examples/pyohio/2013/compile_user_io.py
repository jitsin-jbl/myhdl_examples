
from myhdl import *
from myhdl_tools.boards import get_xilinx_board

from user_io import m_user_io

def compile():
    # get the development board the design is targeting
    brd = get_xilinx_board('xula')
    
    # assign the top-level HDL module (python function)
    # as the top-level
    brd.set_top(m_user_io)
    
    # Set the ports for the design (top-level) and the
    # signal type for the ports.  If the port name matches
    # one of the FPGA default port names they do not need
    # to be remapped.    
    brd.add_port('reset', ResetSignal(0, active=0, async=False),
                 pins=[36], PULLUP=True)
    brd.add_port('button', Signal(bool(0)), pins=[33]) 
    brd.add_port('led', Signal(bool(0)), pins=[32])   

    # set an output directory (path) and convert the MyHDL
    # to Verilog and VHDL and run the tools.  After this
    # is complete a bit file will be ready to load to the
    # FPGA on the xula board.
    brd.path = 'xilinx/ise/user_io/'
    brd.convert(to='verilog')
    brd.convert(to='vhdl')
    brd.run()

if __name__ == '__main__':
    compile()
