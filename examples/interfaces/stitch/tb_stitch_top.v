module tb_stitch_top;

reg clock;
reg reset;
reg adc0_clk;
reg [7:0] adc0_data;
reg [3:0] adc0_ctrl;
reg dac0_clk;
reg [7:0] dac0_data;
reg [3:0] dac0_ctrl;
reg adc1_clk;
reg [7:0] adc1_data;
reg [3:0] adc1_ctrl;
reg dac1_clk;
reg [7:0] dac1_data;
reg [3:0] dac1_ctrl;
reg mii_txclk;
reg [3:0] mii_txd;
reg mii_txen;
reg mii_txer;
reg mii_rxclk;
reg [3:0] mii_rxd;
reg mii_rxdv;
reg mii_rxer;
reg mii_col;
reg mii_cs;

initial begin
    $from_myhdl(
        clock,
        reset,
        adc0_clk,
        adc0_data,
        adc0_ctrl,
        dac0_clk,
        dac0_data,
        dac0_ctrl,
        adc1_clk,
        adc1_data,
        adc1_ctrl,
        dac1_clk,
        dac1_data,
        dac1_ctrl,
        mii_txclk,
        mii_txd,
        mii_txen,
        mii_txer,
        mii_rxclk,
        mii_rxd,
        mii_rxdv,
        mii_rxer,
        mii_col,
        mii_cs
    );
end

stitch_top dut(
    clock,
    reset,
    adc0_clk,
    adc0_data,
    adc0_ctrl,
    dac0_clk,
    dac0_data,
    dac0_ctrl,
    adc1_clk,
    adc1_data,
    adc1_ctrl,
    dac1_clk,
    dac1_data,
    dac1_ctrl,
    mii_txclk,
    mii_txd,
    mii_txen,
    mii_txer,
    mii_rxclk,
    mii_rxd,
    mii_rxdv,
    mii_rxer,
    mii_col,
    mii_cs
);

endmodule
