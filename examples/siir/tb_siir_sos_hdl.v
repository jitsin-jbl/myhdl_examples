module tb_siir_sos_hdl;

reg clk;
reg [23:0] x;
wire [23:0] y;
reg ts;

initial begin
    $from_myhdl(
        clk,
        x,
        ts
    );
    $to_myhdl(
        y
    );
end

siir_sos_hdl dut(
    clk,
    x,
    y,
    ts
);

endmodule
