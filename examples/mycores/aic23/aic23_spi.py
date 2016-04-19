

from myhdl import *
  
def aic23_spi(
    clk,         # system clock
    rst,         # system reset
    data_in,     # parallel data to sent
    data_go,     # command to send data
    busy,        # busy sending data
    AUDIO_CSN,   # Serial config select
    AUDIO_SCLK,  # Serial config clock
    AUDIO_SDIN   # Serial data to AIC23
    ):
    """ SPI interface to configure the AIC23
    """

    clk_cnt   = Signal(modbv(0)[8:])
    bit_cnt   = Signal(intbv(0, max=18, min=0))
    shift_out = Signal(intbv(0)[16:])
    
    csn       = Signal(False)
    sclk      = Signal(False)

    # State types
    States     = enum('IDLE', 'SHIFT', 'LAST_BIT', 'END')
    state  = Signal(States.IDLE)

    sclk_negedge = Signal(False)
    sclk_posedge = Signal(False)

    @always_comb
    def rtl_assignments():
        AUDIO_CSN.next  = csn
        AUDIO_SDIN.next = shift_out[15]

        if not busy or csn:
            AUDIO_SCLK.next  = False
        else:
            AUDIO_SCLK.next = sclk       


    @always(clk.posedge)
    def rtl_simple_sm():
        if rst == False:
            state.next = States.IDLE
            busy.next  = False
        else:
            if state == States.IDLE:
                if data_go:
                    state.next = States.SHIFT
                    busy.next  = True
                else:
                    busy.next  = False
            elif state == States.SHIFT:
                if bit_cnt == 16:
                    state.next = States.LAST_BIT
            elif state == States.LAST_BIT:
                if bit_cnt == 17:
                    state.next = States.END
                    busy.next = False
            elif state == States.END:
                if not data_go: 
                    state.next = States.IDLE

            else:
                assert False, "Invalid State"
                state.next = States.IDLE

    @always(clk.posedge)
    def rtl_sync_outs():
        if rst == False:
            csn.next  = True
            bit_cnt.next = 0
            shift_out.next = data_in
        else:
            if busy and bit_cnt < 18-1:
                if sclk_negedge:
                    csn.next = False
                    bit_cnt.next = bit_cnt + 1
                    if not csn:
                        shift_out.next = (shift_out << 1) & 0xFFFF
            else:
                bit_cnt.next = 0
                shift_out.next = data_in
                csn.next = True
            
    # counter for slower clock, desire a clock that is much slower
    # than the system clock
    CLK_MOD = int(2**8)  # <-- cver issue with verilog power op
    @always(clk.posedge)
    def rtl_slow_clk():
        clk_cnt.next = clk_cnt + 1
        sclk.next    = clk_cnt[7]

    @always_comb
    def rtl_edges():
        sclk_negedge.next = sclk and not clk_cnt[7]
        sclk_posedge.next = not sclk and clk_cnt[7]
        
    return instances()
