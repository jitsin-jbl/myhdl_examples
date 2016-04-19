
from myhdl import *

class StitchBusController:

    def wrapper(self, sp, mii, bb):

        clk, rst = bb.GetControllerSignals()


        @always(clk.posedge)
        def hdl_model():
            pass

        return hdl_model

    wrapper.verilog_code = \
        """
        bb_bus_controller bb(.clk($clk),
                             .rst($rst));
        """
        
