

from myhdl import *

def aic23_i2s(
    clock,       # system clock
    reset,       # system reset
    aic23_bus,   # external I2S bus
    au_bus,      # audio bus
    tst_pts,     # testpoints
    ConfigOpt
    ):

    # Constants given the bit configuration
    MaxBitCnt = ConfigOpt.input_len + 1  # 33, 25, 17, 9
    lhb,llb = (2*MaxBitCnt-1, MaxBitCnt)
    rhb,rlb = (MaxBitCnt, 0)
    # max bit index of the double long register (holds left and right)
    sob = lhb 

    # local aliases
    bclk = aic23_bus.bclk      # CODEC interface clock (12 MHz)
    din = aic23_bus.din        # Audio to CODEC
    dout = aic23_bus.dout      # Audio from CODEC
    lrcin = aic23_bus.lrcin    # left/right for audio to CODEC
    lrcout = aic23_bus.lrcout  # left/right for audio from CODEC

    au_in_l = au_bus.in_l     # to FPGA audio
    au_in_r = au_bus.in_r     # to FPGA audio 
    au_out_l = au_bus.out_l   # from FPGA audio
    au_out_r = au_bus.out_r   # from FPGA audio
    au_mic = au_bus.mic_in    # mic
    au_hp = au_bus.hp_out     # au     
    Ts = au_bus.Ts            # Sample pulse

    # local signals (These are excessively long for low bit configs)
    shift_in  = Signal(intbv(0)[sob+1:])
    shift_out = Signal(intbv(0)[sob+1:])

    _bclk, bclk_n, bclk_p = (Signal(False) for ii in range(3))
    _dout, dout_n, dout_p = (Signal(False) for ii in range(3))
    _lout, lrcout_n, lrcout_p = (Signal(False) for ii in range(3))

    _lin = Signal(False)
    lrcin_n = Signal(False)
    lrcin_p = Signal(False)

    __lin  = Signal(False)
    __lout = Signal(False)
    __dout = Signal(False)
    __bclk = Signal(False)
    
    cnt = Signal(intbv(0, max=MaxBitCnt+1, min=0))
    en_cnt = Signal(False)
    
    # State types
    States     = enum('LEFT_CH_START',   # Falling edge LRCOUT
                  'LEFT_CH_AUDIO',   # Get data enable counter
                  'RIGHT_CH_START',  # Rising edge LRCOUT
                  'RIGHT_CH_AUDIO',  # Right channel audio data
                  )
    state  = Signal(States.LEFT_CH_START)


    @always(clock.negedge)
    def hdl_syncdn():
        __bclk.next = bclk
        __dout.next = dout
        __lin.next  = lrcin
        __lout.next = lrcout

    @always(clock.posedge)
    def hdl_syncdu():        
        _bclk.next = __bclk
        _dout.next = __dout
        _lin.next  = __lin
        _lout.next = __lout


    @always_comb
    def hdl_syncor():
        bclk_n.next = _bclk and not bclk
        bclk_p.next = not _bclk and bclk

        dout_n.next = _dout and not dout
        dout_p.next = not _dout and dout

        lrcin_n.next = _lin and not lrcin
        lrcin_p.next = not _lin and lrcin

        lrcout_n.next = _lout and not lrcout
        lrcout_p.next = not _lout and lrcout


    @always_comb
    def hdl_assignments():
        Ts.next  = lrcin_n
        din.next = shift_out[sob]
        # Use the following for simple test
        #din.next = dout  # Simple Loopback
    
    @always(clock.posedge)
    def hdl_au_in():
        if bclk_p and en_cnt:
            shift_in.next = concat(shift_in[sob:0], _dout)

        if Ts:
            au_in_l.next = shift_in[lhb:llb]  # bit 65 don't care
            au_in_r.next = shift_in[rhb:rlb]  # bit 32 don't care


    mb = len(au_out_l)-1
    @always(clock.posedge)
    def hdl_au_out():
        if Ts:
            shift_out.next = concat(au_out_l[mb], au_out_l,
                                    au_out_r[mb], au_out_r)
        elif bclk_n and en_cnt:
            shift_out.next = concat(shift_out[sob:0], intbv(0)[1:] )


    @always(clock.posedge)
    def hdl_sm():
        if reset == False:
            state.next = States.LEFT_CH_START
            cnt.next   = 0
            en_cnt.next = False
        else:
            if state == States.LEFT_CH_START:
                if lrcin_n:
                    state.next  = States.LEFT_CH_AUDIO
                    en_cnt.next = True
                    
            elif state == States.LEFT_CH_AUDIO:
                if cnt == MaxBitCnt:
                    state.next  = States.RIGHT_CH_START
                    en_cnt.next = False
                    
            elif state == States.RIGHT_CH_START:
                if lrcin_p:
                    state.next = States.RIGHT_CH_AUDIO
                    en_cnt.next = True
                    
            elif state == States.RIGHT_CH_AUDIO:
                if cnt == MaxBitCnt:
                    state.next = States.LEFT_CH_START
                    en_cnt.next = False
            else:
                state.next = States.LEFT_CH_START
                #raise ValueError('Undefined State')


            if en_cnt:
                if bclk_p:
                    cnt.next = cnt + 1
            else:
                cnt.next = 0


    @always_comb
    def rtl_tst_pts():
        tst_pts.next[0]   = bclk
        tst_pts.next[1]   = lrcin
        tst_pts.next[2]   = lrcout
        tst_pts.next[3]   = din
        tst_pts.next[4]   = dout


    return instances()

