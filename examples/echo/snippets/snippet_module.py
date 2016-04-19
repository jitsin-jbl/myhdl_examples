
def echo1(
    clock,                  
    reset,

    # ---- Audio Interface ----
    au_fs,                 # sample rate strobe (data valid in)
    au_in,                 # audio input
    au_out,                # audio output    
    
    # ---- Parameters ----
    C_BD      = 8192,      # Delay Buffer depth / len   BufferLen
    C_BW      = 16,        # Delay Buffer word width    BufferWidth
    C_SR      = 48000,     # Sample Rate                SampleRate
    C_SW      = 24         # Sample width input/output  SampleWidth
    ):
    """Single channel echo

    The following is a basic single channel echo.  An input sample
    is combined with a delayed version of the sample.  This module is 
    the hardware description of the audio echo.  This description will
    be converted to Verilog/VHDL and bit-stream generated using the 
    vendor tools.

    The delay is constant and set by the C_BD parameter.  
    
    Ports
    ---------------------------------------------
      :param au_fs:  input, sample rate strobe
      :param au_in:  input, audio sample input
      :param au_out: output, audio sample output
       
    Configurable Parameters:
    ---------------------------------------------
       :param C_BD:    Delay buffer depth / len
       :param C_BW:    Delay buffer word width
       :param C_SR:    Sample rate
       :param C_SW:    Input sample bit width
       :param XDEVICE: Which Xilinx FPGA (BRAM utilization)
    """

