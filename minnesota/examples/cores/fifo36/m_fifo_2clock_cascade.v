// File: m_fifo_2clock_cascade.v
// Generated by MyHDL 0.9dev
// Date: Sat Jul  5 15:20:19 2014


`timescale 1ns/10ps

module m_fifo_2clock_cascade (
    wclk,
    datain,
    src_rdy_i,
    dst_rdy_o,
    space,
    rclk,
    dataout,
    src_rdy_o,
    dst_rdy_i,
    occupied,
    reset
);


input wclk;
input [35:0] datain;
input src_rdy_i;
output dst_rdy_o;
wire dst_rdy_o;
input [15:0] space;
input rclk;
output [35:0] dataout;
reg [35:0] dataout;
output src_rdy_o;
wire src_rdy_o;
input dst_rdy_i;
input [15:0] occupied;
input reset;

wire fbus_empty;
wire [35:0] dataout_d;
wire rd;
wire fbus_full;
wire wr;
wire gfifo_rrst_n;
reg gfifo_p_aempty_n;
reg gfifo_high;
wire gfifo_fbus_rvld;
wire [6:0] gfifo_rgnext;
reg [6:0] gfifo_wbin;
reg gfifo_wfull;
wire gfifo_wrl;
wire gfifo_wrm;
reg gfifo__rvld1;
reg gfifo_dirset_n;
reg [6:0] gfifo_rbin;
wire gfifo_wrst_n;
reg gfifo_direction;
reg gfifo_afull_n;
reg gfifo_rempty2;
reg [6:0] gfifo_rbnext;
reg [6:0] gfifo_wptr;
reg gfifo_wfull2;
reg [6:0] gfifo_rptr;
reg gfifo_dirclr_n;
reg gfifo_rempty;
reg gfifo__rempty;
reg gfifo_aempty_n;
reg [6:0] gfifo_wbnext;
wire [6:0] gfifo_wgnext;
reg [35:0] gfifo_g_fifomem__din;
reg [6:0] gfifo_g_fifomem__addr_w;
reg [35:0] gfifo_g_fifomem__dout;
reg gfifo_g_fifomem__wr;

reg gfifo_rrst_s [0:2-1];
reg gfifo_wrst_s [0:2-1];
reg [35:0] gfifo_g_fifomem_mem [0:128-1];





assign wr = (src_rdy_i & dst_rdy_o);
assign rd = (dst_rdy_i & src_rdy_o);



assign dst_rdy_o = (!fbus_full);
assign src_rdy_o = (!fbus_empty);


always @(posedge rclk) begin: M_FIFO_2CLOCK_CASCADE_GFIFO_RTL_RD_VLD
    gfifo__rvld1 <= rd;
    gfifo__rempty <= gfifo_rempty;
end


always @(posedge wclk, negedge gfifo_dirset_n, negedge gfifo_dirclr_n) begin: M_FIFO_2CLOCK_CASCADE_GFIFO_RTL_ASYNC_CMP
    if ((!gfifo_dirclr_n)) begin
        gfifo_direction <= 1'b0;
    end
    else if ((!gfifo_dirset_n)) begin
        gfifo_direction <= 1'b1;
    end
    else begin
        if ((!gfifo_high)) begin
            gfifo_direction <= gfifo_high;
        end
    end
end



assign gfifo_wrm = (gfifo_wptr[6] ^ gfifo_rptr[(6 - 1)]);
assign gfifo_wrl = (gfifo_wptr[(6 - 1)] ^ gfifo_rptr[6]);


always @(posedge wclk) begin: M_FIFO_2CLOCK_CASCADE_GFIFO_RTL_WRESET_S
    gfifo_wrst_s[0] <= (!reset);
    gfifo_wrst_s[1] <= gfifo_wrst_s[0];
end



assign gfifo_rgnext = ((gfifo_rbnext >>> 1) ^ gfifo_rbnext);



assign gfifo_wgnext = ((gfifo_wbnext >>> 1) ^ gfifo_wbnext);


always @(posedge rclk, negedge gfifo_rrst_n) begin: M_FIFO_2CLOCK_CASCADE_GFIFO_RTL_RPTR_BIN
    if ((!gfifo_rrst_n)) begin
        gfifo_rbin <= 0;
        gfifo_rptr <= 0;
    end
    else begin
        gfifo_rbin <= gfifo_rbnext;
        gfifo_rptr <= gfifo_rgnext;
    end
end



assign fbus_empty = gfifo_rempty;
assign fbus_full = gfifo_wfull;


always @(rd, gfifo_rbin, gfifo_rempty) begin: M_FIFO_2CLOCK_CASCADE_GFIFO_RTL_RPTR_INC
    if (((!gfifo_rempty) && rd)) begin
        gfifo_rbnext = ((gfifo_rbin + 1) % 128);
    end
    else begin
        gfifo_rbnext = gfifo_rbin;
    end
end



assign dataout_d = gfifo_g_fifomem__dout;


always @(posedge rclk) begin: M_FIFO_2CLOCK_CASCADE_GFIFO_G_FIFOMEM_RTL_RD
    gfifo_g_fifomem__dout <= gfifo_g_fifomem_mem[gfifo_rptr];
end


always @(posedge wclk) begin: M_FIFO_2CLOCK_CASCADE_GFIFO_G_FIFOMEM_RTL_WR
    gfifo_g_fifomem__wr <= wr;
    gfifo_g_fifomem__addr_w <= gfifo_wptr;
    gfifo_g_fifomem__din <= datain;
end


always @(posedge wclk) begin: M_FIFO_2CLOCK_CASCADE_GFIFO_G_FIFOMEM_RTL_MEM
    if (gfifo_g_fifomem__wr) begin
        gfifo_g_fifomem_mem[gfifo_g_fifomem__addr_w] <= gfifo_g_fifomem__din;
    end
end


always @(gfifo_wfull, gfifo_wbin, wr) begin: M_FIFO_2CLOCK_CASCADE_GFIFO_RTL_WPTR_INC
    if (((!gfifo_wfull) && wr)) begin
        gfifo_wbnext = ((gfifo_wbin + 1) % 128);
    end
    else begin
        gfifo_wbnext = gfifo_wbin;
    end
end



assign gfifo_wrst_n = gfifo_wrst_s[1];
assign gfifo_rrst_n = gfifo_rrst_s[1];


always @(posedge rclk, negedge gfifo_aempty_n) begin: M_FIFO_2CLOCK_CASCADE_GFIFO_RTL_RPTR_EMPTY
    if ((!gfifo_aempty_n)) begin
        gfifo_rempty <= 1'b1;
        gfifo_rempty2 <= 1'b1;
    end
    else begin
        gfifo_rempty2 <= (!gfifo_aempty_n);
        gfifo_rempty <= gfifo_rempty2;
    end
end


always @(gfifo_direction, gfifo_rptr, gfifo_wrl, gfifo_wrm, gfifo_wptr, gfifo_wrst_n) begin: M_FIFO_2CLOCK_CASCADE_GFIFO_RTL_ASYNC_CMP_DIR
    gfifo_high = 1'b1;
    if ((gfifo_wrm && (!gfifo_wrl))) begin
        gfifo_dirset_n = 1'b0;
    end
    else begin
        gfifo_dirset_n = 1'b1;
    end
    if ((((!gfifo_wrm) && gfifo_wrl) || (!gfifo_wrst_n))) begin
        gfifo_dirclr_n = 1'b0;
    end
    else begin
        gfifo_dirclr_n = 1'b1;
    end
    if (((($signed({1'b0, gfifo_wptr}) - 1) == gfifo_rptr) && (!gfifo_direction))) begin
        gfifo_p_aempty_n = 1'b0;
    end
    else begin
        gfifo_p_aempty_n = 1'b1;
    end
    if (((gfifo_wptr == gfifo_rptr) && (!gfifo_direction))) begin
        gfifo_aempty_n = 1'b0;
    end
    else begin
        gfifo_aempty_n = 1'b1;
    end
    if (((gfifo_wptr == gfifo_rptr) && gfifo_direction)) begin
        gfifo_afull_n = 1'b0;
    end
    else begin
        gfifo_afull_n = 1'b1;
    end
end


always @(posedge wclk, negedge gfifo_wrst_n, negedge gfifo_afull_n) begin: M_FIFO_2CLOCK_CASCADE_GFIFO_RTL_WPTR_FULL
    if ((!gfifo_wrst_n)) begin
        gfifo_wfull <= 1'b0;
        gfifo_wfull2 <= 1'b0;
    end
    else if ((!gfifo_afull_n)) begin
        gfifo_wfull <= 1'b1;
        gfifo_wfull2 <= 1'b1;
    end
    else begin
        gfifo_wfull <= gfifo_wfull2;
        gfifo_wfull2 <= (!gfifo_afull_n);
    end
end


always @(posedge wclk, negedge gfifo_wrst_n) begin: M_FIFO_2CLOCK_CASCADE_GFIFO_RTL_WPTR_BIN
    if ((!gfifo_wrst_n)) begin
        gfifo_wbin <= 0;
        gfifo_wptr <= 0;
    end
    else begin
        gfifo_wbin <= gfifo_wbnext;
        gfifo_wptr <= gfifo_wgnext;
    end
end


always @(posedge rclk) begin: M_FIFO_2CLOCK_CASCADE_GFIFO_RTL_RRESET_S
    gfifo_rrst_s[0] <= (!reset);
    gfifo_rrst_s[1] <= gfifo_rrst_s[0];
end



assign gfifo_fbus_rvld = (gfifo__rvld1 && (!gfifo__rempty));


always @(posedge rclk) begin: M_FIFO_2CLOCK_CASCADE_RTL_DELAY
    dataout <= dataout_d;
end

endmodule
