/**
 * 
 * Copyright (c) 2009-2012 Christopher L. Felton
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

module sx1_echo
(
 input  wire reset,          ///
 input  wire clk,            ///
 
 /** Misc Dev Board Inputs and Outputs */
 output wire [6:0]  LED,     /// 8 LEDs 

 /** AIC23 CODEC Interface */
 output wire AUDIO_CLK,      ///
 input  wire AUDIO_BCLK,     ///
 output wire AUDIO_DIN,      ///
 input  wire AUDIO_DOUT,     ///
 input  wire AUDIO_LRCIN,    ///
 input  wire AUDIO_LRCOUT,   ///
 input  wire AUDIO_MODE,     /// 

 output wire AUDIO_CSN,      /// Audio CODEC Config select
 output wire AUDIO_SCLK,     /// Audio CODEC serial clock
 output wire AUDIO_SDIN,     /// Audio CODEC serial data in
 
 output wire [7:0] TP_HDR    /// 8 signals to header, testpoints for now
 
);
	
	localparam C_SW  = 24;
	localparam C_SR  = 96000;
	
   //-----------------------------------------------------------
   // Local signals
   //-----------------------------------------------------------
   reg [31:0]  counter;   
   wire        Ts;
   
   wire signed [C_SW-1:0] auil, auir;
   wire signed [C_SW-1:0] auol, auor;
   
   /// Misc assignments
   assign LED  = {counter[24], counter[23], counter[26], auir[23], auil[15], Ts};
   
   //-----------------------------------------------------------
   // Generate a sync reset
   //-----------------------------------------------------------
   /// Create sync reset, all registers are zerod on config,
   /// 8 clock ticks of IFCLK with dcm_locked
	wire srst, _clk, dcm_locked;
   reg [7:0]  rRst;         // Reset Sysnc Pipeline
   reg 	     rff;
	
   assign  srst = ~rRst[7];    // 1 == reset

   always @(posedge _clk) begin  // or negedge RESET
      rRst <= {rRst[6:0], dcm_locked};
   end

   always @(posedge _clk) begin
      rff <= 1'b1;
   end
	
   //-----------------------------------------------------------
   // Create DCM for clocks
   //-----------------------------------------------------------
   dcm12MHz 
     iclk 
       (
	     .CLKIN_IN(clk), 
	     .RST_IN(1'b0),              /// no reset
	     .CLKDV_OUT(clk12MHz), 
	     .CLKIN_IBUFG_OUT(_clk), 
	     .CLK0_OUT(clk48MHz), 
	     .CLKFX_OUT(clk96MHz),
	     .LOCKED_OUT(dcm_locked)
	  );
   
   //-----------------------------------------------------------
   // Counter to drive LEDs
   //-----------------------------------------------------------
   always @(posedge clk12MHz) begin
      counter <= counter + 1;
   end   

   //-----------------------------------------------------------
   // Audio CODEC Interface
   //-----------------------------------------------------------
   aic23 #(C_SR, C_SW)
   CODEC(
	 .clk(clk96MHz),               // clk96MHz
	 .rst(srst),                   // rst
	 .au_in_r(auir),               // audio right in
	 .au_in_l(auil),               // audio left in
	 .au_out_r(auor),              // out to codec
	 .au_out_l(auol),              // out to codec
	 .Ts(Ts),                      // Sample Strobe
	 .AUDIO_BCLK(AUDIO_BCLK),      // Input bit clock
	 .AUDIO_DIN(AUDIO_DIN),        // Serial data in
	 .AUDIO_DOUT(AUDIO_DOUT),      // Serial data out
	 .AUDIO_LRCIN(AUDIO_LRCIN),    // In left/right channel select
	 .AUDIO_LRCOUT(AUDIO_LRCOUT),  // Out left/right channel select
	 //.AUDIO_MODE(AUDIO_MODE),    //
	 .AUDIO_CSN(AUDIO_CSN),        // AIC23b SPI setup chip selectg
	 .AUDIO_SCLK(AUDIO_SCLK),      // AIC23b SPI setup serial clock
	 .AUDIO_SDIN(AUDIO_SDIN),      // AIC23b SPI setup serial data
	 .tst_pts(TP_HDR[5:0])         // Test points
	 );
	 
	 assign TP_HDR[7:6] = 2'b0;
 
   //-----------------------------------------------------------
   // Simple echo
   //-----------------------------------------------------------
   echo1 ECHO_R(clk96MHz, Ts, auir, auor);
   //echo1 ECHO_L(clk96MHz, Ts, auil, auol);
   assign auol = auil;	
	
   //-----------------------------------------------------------
   // Drive a 12MHz clock to the audio CODEC
   //-----------------------------------------------------------
   wire   oclk   = clk12MHz;
   wire   oclk_n = ~clk12MHz;
   OFDDRCPE 
     DDR_CLK 
       (
        .Q(AUDIO_CLK),  // Data output (connect directly to top-level port)
        .C0(oclk),      // 0 degree clock input
        .C1(oclk_n),    // 180 degree clock input
        .CE(1'b1),      // Clock enable input
        .CLR(srst),     // Asynchronous reset input
        .D0(1'b1),      // Posedge data input
        .D1(1'b0),      // Negedge data input
        .PRE(1'b0)      // Asynchronous preset input
	);
   
endmodule
