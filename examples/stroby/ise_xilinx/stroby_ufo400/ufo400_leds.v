// File: stroby.v
// Generated by MyHDL 0.8dev
// Date: Sun Feb  5 10:40:12 2012


`timescale 1ns/10ps

module stroby (
    clk,
    srst,
    led
);


input clk;
input srst;
output [7:0] led;
wire [7:0] led;

reg left_not_right;
reg [23:0] clk_cnt;
reg strobe;
reg [15:0] led_bit_mem;





always @(posedge clk) begin: STROBY_HDL_BEHAVIOR
    if ((srst == 0)) begin
        led_bit_mem <= 1;
        left_not_right <= 1'b1;
        clk_cnt <= 0;
        strobe <= 1'b0;
    end
    else begin
        if ((clk_cnt >= (14400000 - 1))) begin
            clk_cnt <= 0;
            strobe <= 1'b1;
        end
        else begin
            clk_cnt <= (clk_cnt + 1);
            strobe <= 1'b0;
        end
        if (strobe) begin
            if (led_bit_mem[15]) begin
                led_bit_mem <= (1 << (16 - 2));
                left_not_right <= 1'b0;
            end
            else if (led_bit_mem[0]) begin
                led_bit_mem <= 2;
                left_not_right <= 1'b1;
            end
            else begin
                if (left_not_right) begin
                    led_bit_mem <= (led_bit_mem << 1);
                end
                else begin
                    led_bit_mem <= (led_bit_mem >>> 1);
                end
            end
        end
    end
end



assign led = led_bit_mem[(8 + 4)-1:4];

endmodule
