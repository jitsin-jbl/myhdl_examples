// File: siir_hdl.v
// Generated by MyHDL 0.9.0
// Date: Mon Oct 26 14:14:03 2015


`timescale 1ns/10ps

module siir_hdl (
    clk,
    x,
    y,
    ts
);
// This is a simple MyHDL IIR Direct Form I Filter example.  This is intended
// to only be used with the SIIR object.

input clk;
input signed [23:0] x;
output signed [23:0] y;
reg signed [23:0] y;
input ts;

wire signed [48:0] yacc;

reg signed [48:0] ffd [0:2-1];
reg signed [48:0] fbd [0:2-1];




always @(posedge clk) begin: SIIR_HDL_RTL_IIR
    if (ts) begin
        ffd[1] <= ffd[0];
        ffd[0] <= x;
        fbd[1] <= fbd[0];
        fbd[0] <= $signed(yacc[48-1:23]);
    end
    y <= $signed(yacc[48-1:23]);
end



assign yacc = (((((8388608 * x) + (17547599 * ffd[0])) + (9186593 * ffd[1])) - ((-14890123) * fbd[0])) - (6631526 * fbd[1]));

endmodule
