// File: test.v
// Generated by MyHDL 0.9dev
// Date: Sun Nov 24 21:18:19 2013


`timescale 1ns/10ps

module test (

);



reg signed [3:0] a;
reg signed [5:0] q3;
reg signed [5:0] q2;
reg clock;
reg signed [3:0] b;
reg mode;





always @(posedge clock) begin: TEST_TB_DUT_RTL
    reg signed [6-1:0] q1;
    if (mode) begin
        q1 = (a + b);
    end
    else begin
        q1 = (a - b);
    end
    q2 <= (q1 + $signed(q2 >>> 2));
end


always @(posedge clock) begin: TEST_TB_DUT_RTL_PIPED
    reg signed [6-1:0] q1;
    q3 <= (q1 + $signed(q2 >>> 2));
end


initial begin: TEST_TB_CLK
    clock <= 0;
    while (1'b1) begin
        # 3;
        clock <= (!clock);
    end
end


initial begin: TEST_TB_STIM
    integer mm;
    integer aa;
    integer ii;
    integer bb;
    for (mm=0; mm<2; mm=mm+1) begin
        mode <= (mm != 0);
        for (aa=(-8); aa<8; aa=aa+1) begin
            for (bb=(-8); bb<8; bb=bb+1) begin
                a <= aa;
                b <= bb;
                @(posedge clock);
                for (ii=0; ii<5; ii=ii+1) begin
                    @(posedge clock);
                    if ((q3 == q2) !== 1) begin
                        $display("*** AssertionError ***");
                    end
                end
            end
        end
    end
    $finish;
end

endmodule
