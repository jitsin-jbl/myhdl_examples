// -*- verilog -*-
/**
 * @file aic_i2s.v
 *
 * Copyright DSPtronics 2008, 2009, 2010
 * The source files are provided AS IS with no warranty.  DSPtronics
 * is not liable for the use of these source files.  The source files
 * may not be redistributed.
 * 
 * AIC23 is used in master mode.  The serial interface
 * clock rate is automatically configured.
 */
module aic_i2s
#(
  parameter C_SR = 96000, // SAMPLE_RATE
  parameter C_SW = 32     // SAMPLE_WIDTH
)
(
 input  wire clk,     //
 input  wire rst,     //
 input  wire bclk,    //
 output wire din,     //
 input  wire dout,    //
 input  wire lrcin,   //
 input  wire lrcout,  //

 output reg  [C_SW-1:0] au_in_l,
 output reg  [C_SW-1:0] au_in_r,
 input  wire [C_SW-1:0] au_out_l,
 input  wire [C_SW-1:0] au_out_r,
 output wire Ts,
 output wire [5:0] tst_pts

);

   // Little over kill!, could be simplified
   reg [2*C_SW+1:0] shift_in;
   reg [2*C_SW+1:0] shift_out;
   
   wire _bclk, bclk_n, bclk_p;
   wire _dout, dout_n, dout_p;
   wire _lin,  lrcin_n, lrcin_p;
   wire _lout, lrcout_n, lrcout_p;

   localparam S_LEFT_CH_START  = 0,  // Falling Edge LRCOUT
              S_LEFT_CH_AUDIO  = 1,  // Get Data enable counter
              S_RIGHT_CH_START = 2,  // Rising Edge LRCOUT
              S_RIGHT_CH_AUDIO = 3;  // Right channel audio data

   reg [1:0] state, next_state;
   reg       en_cnt; // also do shift
   reg [5:0] cnt;
   
   // Syncronizers and edge, bclk, lrcin, lrcout, dout
   dsync S0(clk, bclk,   _bclk, bclk_n, bclk_p);
   dsync S1(clk, dout,   _dout, dout_n, dout_p);
   dsync S2(clk, lrcin,  _lin,  lrcin_n,  lrcin_p);
   dsync S3(clk, lrcout, _lout, lrcout_n, lrcout_p); 

   assign Ts   = lrcin_n;
   assign din  = shift_out[2*C_SW+1];
   
   always @(posedge clk) begin
      if(bclk_p & en_cnt)
        shift_in <= {shift_in[2*C_SW:0], _dout};
      
      if(Ts) begin
         au_in_l <= shift_in[2*C_SW:C_SW+1];
         au_in_r <= shift_in[C_SW:0]; 
      end   
     
   end

   always @(posedge clk) begin
      if(Ts)
        shift_out <= {au_out_l[C_SW-1], au_out_l, au_out_r[C_SW-1], au_out_r};
      else if(bclk_n & en_cnt)
        shift_out <= {shift_out[2*C_SW:0], 1'b0};
   end

   always @ (posedge clk or posedge rst) begin
      if(rst) begin
         state <= #1 S_LEFT_CH_START;
         cnt   <= #1 6'd0;
      end
      else begin
         state <= #1 next_state;
         if(en_cnt & bclk_p)
           cnt <= #1 cnt + 6'd1;
         else if(~en_cnt)
           cnt <= #1 6'd0;
      end
   end
   
   always @* begin
      next_state = state;
      en_cnt     = 0;

      case(state)
        S_LEFT_CH_START: begin
           if(lrcin_n)
             next_state = S_LEFT_CH_AUDIO;
        end

        S_LEFT_CH_AUDIO: begin
           en_cnt = 1;
           if(cnt == C_SW+1)
             next_state = S_RIGHT_CH_START;
        end

        S_RIGHT_CH_START: begin
           if(lrcin_p)
             next_state = S_RIGHT_CH_AUDIO;
        end

        S_RIGHT_CH_AUDIO: begin
           en_cnt = 1;
           if(cnt == C_SW+1)
             next_state = S_LEFT_CH_START;
        end

        default: next_state = S_LEFT_CH_START;
      endcase
   end // always @ *

   assign tst_pts[0]   = bclk_n;
   assign tst_pts[5:1] = shift_in[4:0];
   
endmodule