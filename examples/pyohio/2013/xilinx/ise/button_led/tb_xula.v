module tb_xula;

reg clock;
reg button;
wire led;

initial begin
    $from_myhdl(
        clock,
        button
    );
    $to_myhdl(
        led
    );
end

xula dut(
    clock,
    button,
    led
);

endmodule
