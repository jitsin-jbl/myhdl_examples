
from myhdl import *
import open_cores.register_file as RF


RegDef = RF.regdict()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AIC23 Control Register
RegDef["AICR"] = {"addr" : 0x00, "width" : 8, "type" : "rw",
                  "bits" : {},
                  "default" : 0x80,  # wb_sel = 1
                  "comment" : "AIC23 Control register"
                  }
RegDef["AICR"]["bits"] = RF.odict(); bits = RegDef["AICR"]["bits"]
bits["WB_SEL"] = {"b" : 7, "width" : 1, "comment" : "1 = Wishbone bus feeds the TX/RX FIFO.\n"  + 
                                                    "0 = Streaming iterface supplies the FIFOs"}
bits["LOOP"]   = {"b" : 1, "width" : 1, "comment" : "Internal loopback"} 
bits["EN"]     = {"b" : 0, "width" : 1, "comment" : "Enable AIC23 interface"}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AIC23 Status Register
RegDef["AISR"] = {"addr" : 0x04, "width" : 8, "type" : "ro",
                  "bits" : {"mode"   : {"b" : 0, "width" : 1, "comment" : "AIC23 interface mode"} ,
                            },
                  "default" : 0x00,  
                  "comment" : "AIC23 Status register"
                  }

# These are shadows of the AIC23 configuration registers, the top 7 msb
# are the address and the bottom 9 lsb bits are the configuraiton bits
# Registers (X no initialize, I init == value)
#
# 0000000 -- Left line input channel volume control   X == 
# 0000001 -- Right line input channel volumen control X == 
# 0000010 -- Left channel headphone volume control    X == 
# 0000011 -- Right channel headphone volume control   X == 
# 0000100 -- Analog audio path control                X ==
# 0000101 -- Digital Audio path control               X ==
# 0000110 -- Power Down Control                       X ==
# 0000111 -- Digital Audio Interface Format           X ==
# 0001000 -- Sample Rate Control                      I == 00 01110 1
# 0001001 -- Digtial Interface Activation             X ==
# 0001111 -- Reset Register                           X ==

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Left Volume Control
RegDef["LVC"]  = {"addr" : 0x20, "width" : 8, "type" : "rw",
                  "bits" : {},  # Bit definition follow register definition                  
                  "default" : "000_0000" + "0_0001_0111",  
                  "comment" : "Left line input channel volume control"
                  }
# Bit defitions, it is convinient to use an order dict for the bit defitions as well
RegDef["LVC"]["bits"] = RF.odict(); bits = RegDef["LVC"]["bits"]
bits["LRS"] = {"b" : 8, "width" : 1,
               "comment" : "Left/right line simultaneous volume/mute update \n" +
               "0=Disable  1=Enable"}
bits["LIM"] = {"b" : 7, "width" : 1,
               "comment" : "Left line input mute  0=Normal  1=Muted"}
bits["LIV"] = {"b" : range(5), "width" : 5,
               "comment" : "Left line input volume control (10111 = 0dB default\n" +
               "11111=+12dB down to 00000=-34dB in 1.5dB steps"} 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Right Volume Control
RegDef["RVC"]  = {"addr" : 0x22, "width" : 8, "type" : "rw",
                  "bits" : {},
                  "default" : "_0001_0111",  #"000_0001" + "0
                  "comment" : "Right line input channel volume control"
                  }
RegDef["RVC"]["bits"] = RF.odict(); bits = RegDef["RVC"]["bits"]
bits["RLS"] = {"b" : 8, "width" : 1,
               "comment" : "Right/left line simultaneous volume/mute update \n" +
               "0=Disable  1=Enable"}
bits["RIM"] = {"b" : 7, "width" : 1,
               "comment" : "Right line input mute\n  0=Normal  1=Muted"}
bits["RIV"] = {"b" : range(5), "width" : 5,
               "comment" : "Left line input volume control (10111 = 0dB default\n" +
               "11111=+12dB down to 00000=-34dB in 1.5dB steps"} 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Left Headphone Control
RegDef["LHC"]  = {"addr" : 0x24, "width" : 8, "type" : "rw",
                  "bits" : {},
                  "default" : "_0000_0000",  #"000_0010" + "0
                  "comment" : "Left channel headphone volume control"
                  }
RegDef["LHC"]["bits"] = RF.odict(); bits = RegDef["LHC"]["bits"]
bits["LRS"] = {"b" : 8, "width" : 1,
               "comment" : "Left/right headphone channel simultaneious volume/mute udpate\n" +
                           "0 = Disable  1 = Enable"}
bits["LZC"] = {"b" : 7, "width" : 1,
               "comment" : "Left-channel zero-cross detect\n"
                           "0 = Off  1 = On"}
bits["LHV"] = {"b" : range(7), "width" : 6,
               "comment" : "Left headphone volume control (1111001 = 0db default)\n" +
                           "1111111 = +6 db, 79 steps between +6 dB and -73 db (mute), 0110000 = -73 db (mute)\n" +
                           "anything below 0110000 does nothing, still muted"}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Right Headphone Control
RegDef["RHC"]  = {"addr" : 0x26, "width" : 8, "type" : "rw",
                  "bits" : {},
                  "default" : "_0000_0000",  #"000_0011" + "0
                  "comment" : "Right channel headphone volume control"
                  }
RegDef["RHC"]["bits"] = RF.odict(); bits = RegDef["RHC"]["bits"]
bits["RLS"] = {"b" : 8, "width" : 1,
               "comment" : "Right/left headphone channel simultaneious volume/mute udpate\n" +
                           "0 = Disable  1 = Enable"}
bits["RZC"] = {"b" : 7, "width" : 1,
               "comment" : "Right-channel zero-cross detect\n"
                           "0 = Off  1 = On"}
bits["RHV"] = {"b" : range(7), "width" : 6,
               "comment" : "Right headphone volume control (1111001 = 0db default)\n" +
                           "1111111 = +6 db, 79 steps between +6 dB and -73 db (mute), 0110000 = -73 db (mute)\n" +
                           "anything below 0110000 does nothing, still muted"}


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Analog audio control
RegDef["AAC"]  = {"addr" : 0x28, "width" : 8, "type" : "rw",
                  "bits" : {},
                  "default" : "_0001_1010",  #"000_0100" + "0
                  "comment" : "Analog audio path control"
                  }
RegDef["AAC"]["bits"] = RF.odict(); bits = RegDef["AAC"]["bits"]
bits["STA"]   = {"b" : range(6,9), "width" : 3, "comment" : "Side-tone attenuation"}
bits["STE"]   = {"b" : 5, "width" : 1, "comment" : "Side-tone enable"}
bits["DAC"]   = {"b" : 4, "width" : 1, "comment" : "DAC Select 0 = DAC off  1 = DAC selected"}
bits["BYP"]   = {"b" : 3, "width" : 1, "comment" : "Bypass 0 = Disabled  1 = Enabled"}
bits["INSEL"] = {"b" : 2, "width" : 1, "comment" : "Input select for ADC 0 = line  1 = Microphone"}
bits["MICM"]  = {"b" : 1, "width" : 1, "comment" : "Microphone mute 0 = Normal  1 = Muted"}
bits["MICB"]  = {"b" : 0, "width" : 1, "comment" : "Microphone boost 0 = db  1 = 20dB"}


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Digital audio control
RegDef["DAC"]  = {"addr" : 0x2A, "width" : 8, "type" : "rw",
                  "bits" : {},
                  "default" : "_0000_0000",  #"000_0101" + "0
                  "comment" : "Digital audio path control"
                  }
RegDef["DAC"]["bits"] = RF.odict(); bits = RegDef["DAC"]["bits"]
bits["DACM"]  = {"b" : 3, "width" : 1, "comment" : "DAC soft mute 0 = Disalbe  1 = Enable"}
bits["DEEMP"] = {"b" : range(1,3), "width" : 2,
                 "comment" : "De-emphasis control\n" +
                             "0 = Disable  1 = 32kHz  2 = 44.1kHz  3 = 48kHz"}
bits["ADCHP"] = {"b" : 0, "width" : 1, "comment" : "ADC high-pass filter"}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Power Down Control
RegDef["PDC"]  = {"addr" : 0x2C, "width" : 8, "type" : "rw",
                  "bits" : {},
                  "default" : "_0000_0010",  #"000_0110" + "0
                  "comment" : "Power down control"
                  }
RegDef["PDC"]["bits"] = RF.odict(); bits = RegDef["PDC"]["bits"]
bits["OFF"]  = {"b" : 7, "width" : 1, "comment" : "Device power"}
bits["CLK"]  = {"b" : 6, "width" : 1, "comment" : "Clock"}
bits["OSC"]  = {"b" : 5, "width" : 1, "comment" : "Oscillator"}
bits["OUT"]  = {"b" : 4, "width" : 1, "comment" : "Outputs"}
bits["DAC"]  = {"b" : 3, "width" : 1, "comment" : "DAC"}
bits["ADC"]  = {"b" : 2, "width" : 1, "comment" : "ADC"}
bits["MIC"]  = {"b" : 1, "width" : 1, "comment" : "Microphone input"}
bits["LINE"] = {"b" : 0, "width" : 1, "comment" : "Line input"}


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Digital Audio Interface Format
RegDef["DAF"]  = {"addr" : 0x2E, "width" : 8, "type" : "rw",
                  "bits" : {},
                  "default" : "_0100_1110",  #"000_0111" + "0
                  "comment" : "Digital audio interface format"
                  }
RegDef["DAF"]["bits"] = RF.odict(); bits = RegDef["DAF"]["bits"]
bits["MS"]     = {"b" : 6, "width" : 1, "comment" : "Master/slave mode"}
bits["LRSWAP"] = {"b" : 5, "width" : 1, "comment" : "DAC lef/right swap"}
bits["LRP"]    = {"b" : 4, "width" : 1, "comment" : "DAC left/right phase"}
bits["IWL"]    = {"b" : range(2,4), "width" : 2,
                  "comment" : "Input bit length\n" +
                  " 00 = 16  01 = 20  10=24  11 = 32"}
bits["FOR"]    = {"b" : range(2), "width" : 2,
                  "comment" : "Data format\n" +
                  "3 = DSP format, frame sync followed by two data words\n"+
                  "2 = I2S format, MSB first, left-1 aligned\n"+
                  "1 = MSB first, left aligned\n"+
                  "0 = MSB first, right aligned"}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Sample Rate Control
RegDef["SRC"]  = {"addr" : 0x30, "width" : 8, "type" : "rw",
                  "bits" : {},
                  "default" : "_1001_1101",  #"000_1000" + "0
                  "comment" : "Sample rate control"
                  }
RegDef["SRC"]["bits"] = RF.odict(); bits = RegDef["SRC"]["bits"]

bits["CLKOUT"] = {"b" : 7, "width" : 1, "comment" : "clock output divider, 1 = MCLK/2"}
bits["CLKIN"]  = {"b" : 6, "width" : 1, "comment" : "clock input divider, 1 = MCLK/2"}
bits["SR"]     = {"b" : range(2,6), "width" : 4, "comment" : "Sampling rate control, see datasheet"}
bits["BOSR"]   = {"b" : 1, "width" : 1, "comment" : "Base oversample rate, see datasheet"}
bits["USB"]    = {"b" : 0, "width" : 1, "comment" : "Clock mode select"}


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Digital Interface Activation
RegDef["DIA"]  = {"addr" : 0x32, "width" : 8, "type" : "rw",
                  "bits" : {},
                  "default" : "_0000_0001",  #"000_1001" + "0
                  "comment" : "Digital interface activation"
                  }
RegDef["DIA"]["bits"] = RF.odict(); bits = RegDef["DIA"]["bits"]
bits["ACT"] = {"b" : 0, "width" : 1, "comment" : "Activate interface 1 = Active"}


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Reset Regester
RegDef["RST"]  = {"addr" : 0x34, "width" : 8, "type" : "rw",
                  "bits" : {},
                  "default" : "_0000_0000",  #"000_1111" + "0
                  "comment" : "Reset register, write 0 to this register to trigger a reset"
                  }
RegDef["RST"]["bits"] = RF.odict(); bits = RegDef["RST"]["bits"]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Program Configuration Register
RegDef["PGM"]  = {"addr" : 0x36, "width" : 8, "type" : "rw",
                  "bits" : {},
                  "default" : "_0000_0000",  #"000_0000" + "0
                  "comment" : "Program the configuration"
                  }
RegDef["PGM"]["bits"] = RF.odict(); bits = RegDef["PGM"]["bits"]
bits["go"] = {"b" : 0, "width" : 1, "comment" : "1 = Program the configuration\n" +
                                              "0 = No action"}




unused = RF.GetRegisterFileSignals(RegDef)

# List of Signals (Register File) index for each register
aicr_i = RegDef['AICR']['index']
aisr_i = RegDef['AICR']['index']
lvc_i  = RegDef['LVC']['index']
rvc_i  = RegDef['RVC']['index']
lhc_i  = RegDef['LHC']['index']
rhc_i  = RegDef['RHC']['index']
aac_i  = RegDef['AAC']['index']
dac_i  = RegDef['DAC']['index']
pdc_i  = RegDef['PDC']['index']
daf_i  = RegDef['DAF']['index']
src_i  = RegDef['SRC']['index']
dia_i  = RegDef['DIA']['index']
rrst_i = RegDef['RST']['index']
pgm_i  = RegDef['PGM']['index']







