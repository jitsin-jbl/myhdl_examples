

module dsync
(
 input  wire clk,
 input  wire d,
 output reg  q,
 output wire n,
 output wire p
 );
   
   reg  iq, dq;
   
   assign n = q & ~dq;
   assign p = ~q & dq;
   
   always @(negedge clk) begin
      iq  <= d;
   end
   
   always @(posedge clk) begin
      dq  <= iq;
   end
   
   always @(posedge clk) begin
      q  <= dq;
   end
   
endmodule // dsync
