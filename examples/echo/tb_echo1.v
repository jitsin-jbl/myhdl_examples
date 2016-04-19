module tb_echo1;

reg clock;
reg reset;
reg au_fs;
reg [23:0] au_in;
wire [23:0] au_out;

initial begin
    $from_myhdl(
        clock,
        reset,
        au_fs,
        au_in
    );
    $to_myhdl(
        au_out
    );
end

echo1 dut(
    clock,
    reset,
    au_fs,
    au_in,
    au_out
);

endmodule
