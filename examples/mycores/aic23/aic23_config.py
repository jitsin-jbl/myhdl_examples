
import argparse
from myhdl import intbv

class Aic23Config(argparse.Namespace):
    """
    This object is used to set the configuration for the AIC23.

    List of configuration options:
       * sample_rate : Set the sample rate, 8,32,44.1,48,96kHz
       * input_len : input word length.  Audio sample size in bits, 16,20,24,32
       * left and right : channel settings, each left and right contains
         the following
          * mute : mute line in
          * lock : left and right updated at the same time
          * volume : line in volume
          * hp_lock : headphone, left and right updated at the same time
          * hp_zero_cross : headphone, check for zero-crossing
          * hp_volume : headphone volume
    """
    def __init__(self, parser=None):
        argparse.Namespace.__init__(
            self,
            sample_rate=32,  # sample rate in kHz
            input_len=16     # input word length
            )
        self.left = argparse.Namespace(mute=False, lock=False, volume=23,
                                       hp_lock=False, hp_zero_cross=True,
                                       hp_volume=121)
        self.right = argparse.Namespace(mute=False, lock=False, volume=23,
                                       hp_lock=False, hp_zero_cross=True,
                                       hp_volume=121)
   
    def __str__(self):
        # make a simple table k dots v where is around 38
        # #dots = 38-len(k)-3
        s = ''
        for k,v in self.__dict__.items():
            if isinstance(v, argparse.Namespace):
                s += '   %s :\n' % (k)
                for ek,ev in v.__dict__.items():
                    nd = 38-len(ek)-6
                    s += '      %s %s %s\n' % (ek, '.'*nd, ev)
            else:
                nd = 38-len(k)-3
                s += '   %s %s %s\n' % (k, '.'*nd, v)
        return s

    def BuildRom(self):
        """
        Given the configuration options build the "ROM".  The "ROM"
        is the values the registers in the AIC23 will be programmed 
        as.
        The following are the registers that are programmed
          LVC :00: Left line input channel volume control
          RVC :01: Right line input channel volume control
          LHC :02: Left channel headphone volume control
          RHC :03: Right channel headphone volume control
          AAC :04: Analog audio path control
          DAC :05: Digital audio path control
          PDC :06: Power down control
          DAF :07: Digital audio interface format
          SRC :08: Sample rate control
          DIA :09: Digital interface activation
          RST :0F: Reset register

          Reference : http://www.ti.com/lit/ds/symlink/tlv320aic23b.pdf
          
          The following will convert the instance attributes to the 
          register settings.  The following is fairly dense because it 
          includes majority of the documentation for the registers.
        """
        # Each register is 9 bits and a 7 bit address.  Each control transfer
        # is 16bits over SPI (this core uses the SPI as the control interface).
        
        # Channel volume control registers
        #             D8    D7    D6    D5    D4    D3    D2    D1    D0
        # Function   LRS   LIM    x     x    LIV4  LIV3  LIV2  LIV1  LIV0
        # Default     0     1     0     0     1     0     1     1     1
        #    LRS : Left/right line simultaneous volume/mute update (lock)
        #          Simultaneous update 0 = Disabled   1 = Enabled
        #    LIM : Line inmput mute
        #          Line input mute     0 = Normal     1 = Muted
        #    LIV : Line input volume
        #          
        LVC = intbv('0_0001_0111') # left line unmute, volume = 10111, Default 0_1001_0111
        RVC = intbv('0_0001_0111') # right line unmute, volume = 10111, Default 0_1001_0111
        LVC[8] = 1 if self.left.lock else 0
        LVC[7] = 1 if self.left.mute else 0
        LVC[5:] = self.left.volume
        RVC[8] = 1 if self.right.lock else 0
        RVC[7] = 1 if self.right.mute else 0
        RVC[5:] = self.right.volume
                
        # Headphone volume control registers
        #             D8    D7    D6    D5    D4    D3    D2    D1    D0
        # Function  
        # Default
        LHC = intbv('0_0000_0000') # all disable, Default 0_1111_1001
        RHC = intbv('0_0000_0000') # all disable, Default 0_1111_1001    
        # @todo : headphone controls

        #             D8    D7    D6    D5    D4    D3    D2    D1    D0
        # Function  
        # Default
        AAC = intbv('0_0001_1010') # Side tone disable, DAC select, Default 0_0000_1010
        # @todo : 

        #             D8    D7    D6    D5    D4    D3    D2     D1     D0
        # Function    x     x     x     x     x    DACM  DEEMP1 DEEMP0 ADCHP
        # Default     0     0     0     0     0     1     0      0      0
        #    DACM DAC soft mute        0 = Disabled   1 = Enabled
        #    DEEMP deemphasis         00 = Disabled   01 = 32kHz
        #           
        DAC = intbv('0_0000_0000') # disable all, Default 0_0000_1000

        # Power Down Control
        #             D8    D7    D6    D5    D4    D3    D2    D1    D0
        # Function  
        # Default        
        PDC = intbv('0_0000_0010') # power down mic, Default 0_0000_0111
        
        # Digital Audio Interface Format
        #             D8    D7    D6    D5     D4    D3    D2    D1    D0
        # Function    x     x    MS    LRSWAP LRP   IWL1  IWL0  FOR1  FOR0
        # Default     0     0     0     0      0     0     0     0     1
        #  MS     Master/slave mode    0 = Slave      1 = Master
        #
        #  LRSWAP DAC left/right swap  0 = Disable    1 = Enable
        #
        #  LRP    DAC left/right phase 0 = right channel on, LRCIN high
        #                              1 = right channel on, LRCIN low, DSP mode
        # 
        #  IWL    Input bit length    00 = 16  01=20  10=24  11=32
        # 
        #  FOR    Data format         00 = I2S MSB first, right aligned
        #                             01 = I2S MSB first left aligned
        #                             10 = I2S MSB first left-1 alighed
        #                             11 = DSP format, frame sync followed by two data words
        DAF = intbv('0_0100_1110') # Master mode, 32 bit word, I2S format
        iwl_t = {16:0, 20:1, 24:2, 32:3}
        DAF[4:2] = iwl_t[self.input_len]

        # Sample Rate Control
        #             D8    D7     D6    D5    D4    D3    D2    D1    D0
        # Function    x    CLKOUT CLKIN SR3   SR2   SR1   SR0   BOSR  USB/Normal
        # Default     0     0      0     1     0     0     0     0     0
        #  
        SRC = intbv('0_1001_1101') # clkout/2, SR= 0111 96kHz, USB mode
        self.sample_rate = int(self.sample_rate)
        sr_t = {8:(3,0), 32:(8,0), 44:(8,1), 48:(0,0), 96:(3,0)}
        SRC[6:2] = sr_t[self.sample_rate][0]
        SRC[1] = sr_t[self.sample_rate][1]
        

        DIA = intbv('0_0000_0001') # activate interface, Default 0_0000_0000
        RST = intbv('0_0000_0000') # no reset, Default 0_0000_0000

        # create two tuple of ints(intbv) first for the values the secod
        # for the address.
        config_rom = tuple(map(int, (LVC, RVC, LHC, RHC, AAC, DAC, PDC, DAF, SRC, DIA, RST)))
        config_addr = (0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09 ,0x0F)
        assert len(config_rom) == len(config_addr)

        return config_rom, config_addr


        
