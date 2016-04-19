// -*- verilog -*-
/**
 * Copyright DSPtronics 2008, 2009, 2010
 * The source files are provided AS IS with no warranty.  DSPtronics
 * is not liable for the use of these source files.  The source files
 * may not be redistributed.
 * 
 * Simple interface to the AIC23 CODEC.  Currently hardcoded for a 
 * set configuration.
 * 
 * Default to 96kHz Sample rate and 32bit word.
 */

`resetall
//synopsys translate_off
`default_nettype none    // Must explicitly declare all signals.
//synopsys translate_on
  
module aic23
#(
  parameter C_SR = 96000, // SAMPLE_RATE
  parameter C_SW = 32     // SAMPLE_WIDTH
)
(
input  wire clk,
input  wire rst,

// [CODEC Interface to FPGA Logic]
output wire [C_SW-1:0] au_in_r,   // Samples to FPGA Logic
output wire [C_SW-1:0] au_in_l,   //
input  wire [C_SW-1:0] au_out_r,  // Samples from FPGA Logic
input  wire [C_SW-1:0] au_out_l,  // 
output wire Ts,               // Sample Rate Pulse, Interrupt Signal

// [Bus Interface for Configuration] \TODO

// [External CODEC Interface to AIC23]
//         [Signal Name][AIC23 Pin][FPGA Pin][---Comment--------------------]  | 
//output wire AUDIO_CLK,    // 25     AB3     - MCLK, external clock input 12MHz |  
input  wire AUDIO_BCLK,     //  3     F3      - I2S Serial-bit clock             |
output wire AUDIO_DIN,      //  4     J21     - I2S                              |
input  wire AUDIO_DOUT,     //  6     B13     - I2S                              |
input  wire AUDIO_LRCIN,    //  5     W4      - I2S DAC-word clock signal        |
input  wire AUDIO_LRCOUT,   //  7     AB2     - I2S ADC-word clock signal        |
//output wire AUDIO_MODE,   // 22     AA2     - 0 - 2 wire, 1- SPI               |
output wire AUDIO_CSN,      // 21     AC25    - Control Mode Chip Select         |
output wire AUDIO_SCLK,     // 24     R4      - Control-port Serial clock        |
output wire AUDIO_SDIN,     // 23     AD2     - Control-port Serial data         |

output wire [5:0] tst_pts 
);
   
   //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   // --[Continuous Assignments]--
   //assign AUDIO_MODE = 1'b1;     // SPI Mode

   
   //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   // --[AIC23 Setup]--
   aic23_setup #(C_SR, C_SW)
     SETUP
     (
      .clk(clk),
      .rst(rst),
      .AUDIO_CSN(AUDIO_CSN),
      .AUDIO_SCLK(AUDIO_SCLK),
      .AUDIO_SDIN(AUDIO_SDIN)
      );

   
   //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   // --[I2S]--
   aic_i2s #(C_SR, C_SW)
     I2S
       (
        .clk(clk),
        .rst(rst),
        .bclk(AUDIO_BCLK),
        .din(AUDIO_DIN),
        .dout(AUDIO_DOUT),
        .lrcin(AUDIO_LRCIN),
        .lrcout(AUDIO_LRCOUT),
        .au_in_l(au_in_l),
        .au_in_r(au_in_r),
        .au_out_l(au_out_l),
        .au_out_r(au_out_r),
        .Ts(Ts),
        .tst_pts(tst_pts)
        );

   
endmodule