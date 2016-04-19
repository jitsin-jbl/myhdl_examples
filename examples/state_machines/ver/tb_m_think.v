module tb_m_think;

reg clock;
reg reset;
wire thinking;
wire sending;
wire [43:0] sent;

initial begin
    $from_myhdl(
        clock,
        reset
    );
    $to_myhdl(
        thinking,
        sending,
        sent
    );
end

m_think dut(
    clock,
    reset,
    thinking,
    sending,
    sent
);

endmodule
