// File: m_think.v
// Generated by MyHDL 0.8
// Date: Fri Sep  6 14:16:54 2013


`timescale 1ns/10ps

module m_think (
    clock,
    reset,
    thinking,
    sending,
    sent
);


input clock;
input reset;
output thinking;
reg thinking;
output sending;
reg sending;
output [43:0] sent;
wire [43:0] sent;

reg [3:0] state;
reg [43:0] lsent;





always @(posedge clock, negedge reset) begin: M_THINK_RTL
    if (reset == 0) begin
        thinking <= 0;
        sending <= 0;
        state <= 4'b0001;
        lsent <= 0;
    end
    else begin
        thinking <= 1'b0;
        sending <= 1'b0;
        casez (state)
            4'b???1: begin
                state <= 4'b0010;
            end
            4'b??1?: begin
                thinking <= 1'b1;
                state <= 4'b0100;
            end
            4'b?1??: begin
                sending <= 1'b1;
                state <= 4'b1000;
            end
            4'b1???: begin
                lsent <= (lsent + 1);
                state <= 4'b0001;
            end
            default: begin
                if (1'b0 !== 1) begin
                    $display("*** AssertionError ***");
                end
            end
        endcase
    end
end

endmodule