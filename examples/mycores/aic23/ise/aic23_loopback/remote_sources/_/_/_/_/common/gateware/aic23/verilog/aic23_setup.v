/**
 * @file aic23_setup.v
 * 
 * Copyright DSPtronics 2008, 2009, 2010
 * The source files are provided AS IS with no warranty.  DSPtronics
 * is not liable for the use of these source files.  The source files
 * may not be redistributed.
 * 
 */

`resetall
//synopsys translate_off
`default_nettype none    // Must explicitly declare all signals.
//synopsys translate_on
  
module aic23_setup
#(
  parameter SAMPLE_RATE  = 96000,
  parameter SAMPLE_WIDTH = 32
)
(
 input  wire  clk,
 input  wire  rst,
 output wire  AUDIO_CSN,
 output wire  AUDIO_SCLK,
 output wire  AUDIO_SDIN
);   
   //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   // -- [Start Up State Machine]--
   //localparam S_RESET,
   //localparam S_INIT_REG0,
   
   // Registers (X no initialize, I init == value)
   // 0000000 -- Left line input channel volume control   X == 
   // 0000001 -- Right line input channel volumen control X == 
   // 0000010 -- Left channel headphone volume control    X == 
   // 0000011 -- Right channel headphone volume control   X == 
   // 0000100 -- Analog audio path control                X ==
   // 0000101 -- Digital Audio path control               X ==
   // 0000110 -- Power Down Control                       X ==
   // 0000111 -- Digital Audio Interface Format           X ==
   // 0001000 -- Sample Rate Control                      I == 00 01110 1
   // 0001001 -- Digtial Interface Activation             X ==
   // 0001111 -- Reset Register                           X ==
   
   // AIC23 Register Addresses
   localparam R_LVC = 7'b000_0000,  // Left Volume Control
              R_RVC = 7'b000_0001,  // Right Volume Control
              R_LHC = 7'b000_0010,  // Left Headphone Volume Control
              R_RHC = 7'b000_0011,  // Right Headphone Volume Control
              R_AAC = 7'b000_0100,  // Analog Audio Path Control
              R_DAC = 7'b000_0101,  // Digital Audio Path Control
              R_PDC = 7'b000_0110,  // Power Down Control
              R_DAF = 7'b000_0111,  // Digital Audio Interface Format
              R_SRC = 7'b000_1000,  // Sample Rate Control
              R_DIA = 7'b000_1001,  // Digital Interface Activation
              R_RST = 7'b000_1111;  // Reset Register

   // AIC23 Register Addresses Init Value
   localparam I_LVC = 9'b0_0001_0111,  // 0_0001_0111
              I_RVC = 9'b0_0001_0111,  // 0_0001_0111
              I_LHC = 9'b0_0000_0000,  // 
              I_RHC = 9'b0_0000_0000,  // 
              I_AAC = 9'b0_0001_0010,  // 
              I_DAC = 9'b0_0000_0000,  // 
              I_PDC = 9'b0_0000_0010,  // 0 0000 0010
     
              I_DAF = 9'b0_0100_1110,  // 0 0100 1110  32 bit
              //I_DAF = 9'b0_0100_1010,  // 24bit
              
              I_SRC = 9'b0_0001_1101,  // 96kHz sample
              //I_SRC = 9'b0_0001_1001,  // 32kHz sample
              //I_SRC = 9'b0_0000_1101,  // 8kHz sample
				  
              I_DIA = 9'b0_0000_0001,  // 
              I_RST = 9'b0_0000_0000;  // 

   // States
   localparam S_IDLE = 0,
              S_RGO  = 1,  // Init Reg 1
              S_INC  = 2,  //
              S_WAIT = 3,
              S_END  = 4;  // Done

   reg [15:0] aic_c;      // Control Data
   reg        aic_c_go;   // Send Control Data
   wire       aic_c_busy; // Sending Data

   
   reg [3:0] state, next_state;
   reg       _go;
   reg [3:0] reg_cnt;

   
   //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   // State Register
   always @(posedge clk or posedge rst) begin
      if(rst) begin
         state    <= S_IDLE;
         aic_c_go <= 1'b0;
         reg_cnt  <= 4'd0;
      end
      else begin
         state <= next_state;
         if(_go & ~aic_c_busy)
           aic_c_go <= 1'b1;
         else
           aic_c_go <= 1'b0;
         if(state == S_INC)
           reg_cnt <= reg_cnt + 4'd1;
      end
   end

   
   //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   // Next State
   always @(*) begin
      // Defaults
      next_state = state;
      aic_c = 16'h0000;
      _go   = 0;
      
      case(state)
        S_IDLE: begin
           next_state = S_RGO;
        end
        
        S_RGO: begin
           _go   = 1'b1;
           case(reg_cnt)
             0: aic_c = {R_LVC, I_LVC};
             1: aic_c = {R_RVC, I_RVC};
             2: aic_c = {R_LHC, I_LHC};
             3: aic_c = {R_RHC, I_RHC};
             4: aic_c = {R_AAC, I_AAC};
             5: aic_c = {R_DAC, I_DAC};
             6: aic_c = {R_PDC, I_PDC};
             7: aic_c = {R_DAF, I_DAF};
             8: aic_c = {R_SRC, I_SRC};
             9: aic_c = {R_DIA, I_DIA};
             default: aic_c = {R_LVC, I_LVC};
           endcase
           if(aic_c_go)
             next_state = S_INC;
        end 
   
        S_INC: begin
           next_state = S_WAIT;
        end
             
        S_WAIT: begin
           if(~aic_c_busy) begin
              if(reg_cnt == 10)
                next_state = S_END;
              else
                next_state = S_RGO;
           end
        end

        S_END: begin
           next_state = S_END; // Nothing
        end

      endcase
   end


   //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   // --[SPI Controller]--
   aic_spi
	    SPI
     (
      .clk(clk),               // System Clock
      .rst(rst),               // System Reset
      .data_in(aic_c),         // 16-bit data in, Address/Data 
      .data_go(aic_c_go),      // Pulse data to go
      .busy(aic_c_busy),       // Busy sending data
      .AUDIO_CSN(AUDIO_CSN),   // SPI chip select
      .AUDIO_SCLK(AUDIO_SCLK), // SPI clock
      .AUDIO_SDIN(AUDIO_SDIN)  // SPI data input
      );


endmodule