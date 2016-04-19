module tb_firfilt;

   reg [15:0] sig_in;
   wire [15:0] sig_out;
   reg 	    clk;
   reg rst;
   

   initial begin
      $from_myhdl(
		  sig_in,
		  clk,
		  rst
		  );
      $to_myhdl(
		sig_out
		);
   end

   firfilt dut(
	       sig_in,
	       sig_out,
	       clk,
	       rst
	       );
   
   initial begin
      $dumpfile("test_firfilt_cosim.vcd");
      $dumpvars(0,dut);      
   end
   
endmodule



   