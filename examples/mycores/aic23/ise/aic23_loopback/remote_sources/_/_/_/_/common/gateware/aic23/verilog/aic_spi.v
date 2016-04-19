// -*- verilog -*-
/**
 * @file aic_spi.v
 * 
 * Copyright DSPtronics 2008, 2009, 2010
 * The source files are provided AS IS with no warranty.  DSPtronics
 * is not liable for the use of these source files.  The source files
 * may not be redistributed.
 *
 * This is a simple SPI interface to configure the AIC23 
 * CODEC.  One the Cyclone DSP board a 50 MHz 
 */ 

`resetall
//synopsys translate_off
`default_nettype none    // Must explicitly declare all signals.
//synopsys translate_on

module aic_spi
(
 input  wire clk,               //
 input  wire rst,               //
 input  wire [15:0] data_in,    //
 input  wire data_go,           //
 output wire busy,              //
 output wire AUDIO_CSN,         //
 output wire AUDIO_SCLK,        //
 output wire AUDIO_SDIN         //
);

   reg  [7:0] clk_cnt;          //
   reg        _ccnt;            //
   reg        ce;               //
   reg [4:0]  bit_cnt;          //
   reg [15:0] shift_out;        //

   reg        sclk;
   reg        csn;

   assign AUDIO_CSN  = csn;
   assign AUDIO_SCLK = sclk;
   assign AUDIO_SDIN = shift_out[15];

   localparam S_IDLE  = 0,
              S_SHIFT = 1;

   reg [1:0] state, next_state;
   
   /**
    * Simple state machine, parallel to serial, send 16 bit
    * AIC control information.
    */
   always @(posedge clk or posedge rst) begin
      if(rst) begin
         //sclk      <= #1 1'b1;
         csn       <= #1 1'b1;
         bit_cnt   <= #1 5'h0;
         shift_out <= #1 16'h00;
      end
      else begin
         state <= next_state;
         if(busy) begin
            if(ce) begin
               //sclk  <= #1 ~sclk;
               // Negedge 1 -> 0
               if(sclk) begin
                  csn       <= #1 1'b0;
                  bit_cnt   <= #1 bit_cnt + 5'd1;
                  if(~csn)
                    shift_out <= #1 {shift_out[14:0],1'b0}; 
               end               
            end
         end
         else begin
            bit_cnt   <= #1 4'h0;
            shift_out <= #1 data_in;
            //sclk      <= #1 1'b1;
            csn       <= #1 1'b1;
         end
      end
   end // always @ (posedge clk or posedge rst)

   always @(posedge clk or posedge rst) begin
      if(rst) begin
         sclk      <= #1 1'b1;
      end
      else begin
         if(ce) begin
            sclk  <= #1 ~sclk;
         end
      end
   end

   always @(*) begin
      // defaults
      next_state = state;
      
      case(state)
        S_IDLE: begin
           if(data_go)
             next_state = S_SHIFT;
        end

        S_SHIFT: begin
           if(bit_cnt >= 17)
             next_state = S_IDLE;
        end
        
        default: begin
           $display("Invalid State");
           next_state   = S_IDLE;
        end
      endcase
   end

   assign busy = (state != S_IDLE);

   /**
    * Counter for slower clock.  Want a clock that is much
    * slower than the system clock, ~ 100 time less (100MHz system clock).
    * 
    */
   always @(posedge clk or posedge rst) begin
      if(rst) begin
         clk_cnt <= 8'h00;
         _ccnt   <= 1'b0;
         ce      <= 1'b0;
      end
      else begin
         clk_cnt <= clk_cnt + 8'd1;
         _ccnt   <= clk_cnt[7];
         if( _ccnt != clk_cnt[7])
           ce <= 1'b1;
         else
           ce <= 1'b0;
      end
   end



endmodule   