// File: xula.v
// Generated by MyHDL 0.8
// Date: Fri Nov 29 10:00:06 2013


`timescale 1ns/10ps

module xula (
    clock,
    reset,
    button,
    led
);
// blink the LED, button go faster
// Blink the LED at a default slow rate, each time the button
// is pressed increase the blink rate.  Once the blink rate
// reaches a maximum rate start over with the slow rate.
// The rate limits are controlled by parameters:
// *max_blink* and *min_blink* in seconds.  The button also needs
// to be debounce.  Only one rate change is desired per button
// press, to achieve this the button needs to be debounced.  The
// debounce rate is also controlled by a parameter *debounce* which
// is also in seconds.

input clock;
input reset;
input button;
output led;
reg led;

reg [25:0] blink_count;
reg [21:0] pressed_count;
reg _button;
reg [21:0] button_count;
reg [25:0] blink_count_max;





always @(posedge clock) begin: XULA_RTL_DEBOUNCE
    if (reset == 0) begin
        button_count <= 0;
        pressed_count <= 0;
        _button <= 0;
    end
    else begin
        if ((button == 1'b0)) begin
            if ((pressed_count < 1200000)) begin
                pressed_count <= (pressed_count + 1);
            end
        end
        else begin
            if ((button_count >= 1200000)) begin
                _button <= 1'b1;
                button_count <= 0;
            end
            else begin
                _button <= 1'b0;
            end
            if ((pressed_count > 0)) begin
                button_count <= pressed_count;
                pressed_count <= 0;
            end
        end
    end
end


always @(posedge clock) begin: XULA_RTL_BLINK
    if (reset == 0) begin
        blink_count_max <= 24000000;
        led <= 0;
        blink_count <= 0;
    end
    else begin
        if (_button) begin
            if ((blink_count_max > 396000)) begin
                blink_count_max <= (blink_count_max >>> 1);
            end
            else begin
                blink_count_max <= 24000000;
            end
        end
        else begin
            if ((blink_count < blink_count_max)) begin
                blink_count <= (blink_count + 1);
            end
            else begin
                led <= (!led);
                blink_count <= 1;
            end
        end
    end
end

endmodule
