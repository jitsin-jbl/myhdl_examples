module tb_simple_top;

reg clock;
reg reset;
reg [7:0] buttons;
wire [7:0] leds;

initial begin
    $from_myhdl(
        clock,
        reset,
        buttons
    );
    $to_myhdl(
        leds
    );
end

simple_top dut(
    clock,
    reset,
    buttons,
    leds
);

      initial begin
      $dumpfile("test_simple_cosim.vcd");
      $dumpvars(0,dut);      
   end


endmodule
