// File: complex_top.v
// Generated by MyHDL 0.8dev
// Date: Mon Aug 27 21:39:33 2012


`timescale 1ns/10ps

module complex_top (
    clock,
    reset,
    a_real,
    a_imag,
    b_real,
    b_imag,
    c_real,
    c_imag
);


input clock;
input reset;
input signed [3:0] a_real;
input signed [3:0] a_imag;
input signed [3:0] b_real;
input signed [3:0] b_imag;
output signed [8:0] c_real;
reg signed [8:0] c_real;
output signed [8:0] c_imag;
reg signed [8:0] c_imag;






always @(posedge clock, negedge reset) begin: COMPLEX_TOP_G_CM_HDL_MULT
    if (reset == 0) begin
        c_real <= 0;
        c_imag <= 0;
    end
    else
        c_real <= ((a_real * b_real) - (a_imag * b_imag));
        c_imag <= ((a_real * b_imag) + (a_imag * b_real));
    end
    
    endmodule
