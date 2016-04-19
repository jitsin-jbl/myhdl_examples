-- File: firfilt.vhd
-- Generated by MyHDL 0.8dev
-- Date: Sat Jun 30 20:42:36 2012


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_08dev.all;

entity firfilt is
    port (
        sig_in: in signed (15 downto 0);
        sig_out: out signed (15 downto 0);
        clk: in std_logic;
        rst: in std_logic
    );
end entity firfilt;


architecture MyHDL of firfilt is

type t_array_taps is array(0 to 33-1) of signed (15 downto 0);
signal taps: t_array_taps;

begin




FIRFILT_HDL_SOP: process (clk) is
    variable sop: integer;
    variable c: integer;
begin
    if rising_edge(clk) then
        if to_boolean(rst) then
            for ii in 0 to 33-1 loop
                taps(ii) <= "0000000000000000";
            end loop;
            sig_out <= "0000000000000000";
        else
            sop := 0;
            for ii in 0 to 33-1 loop
                if (ii = 0) then
                    taps(ii) <= sig_in;
                else
                    taps(ii) <= taps((ii - 1));
                end if;
                case ii is
                    when 0 => c := 7;
                    when 1 => c := 40;
                    when 2 => c := 82;
                    when 3 => c := 120;
                    when 4 => c := 117;
                    when 5 => c := 27;
                    when 6 => c := -174;
                    when 7 => c := -453;
                    when 8 => c := -701;
                    when 9 => c := -746;
                    when 10 => c := -416;
                    when 11 => c := 391;
                    when 12 => c := 1645;
                    when 13 => c := 3154;
                    when 14 => c := 4607;
                    when 15 => c := 5659;
                    when 16 => c := 6043;
                    when 17 => c := 5659;
                    when 18 => c := 4607;
                    when 19 => c := 3154;
                    when 20 => c := 1645;
                    when 21 => c := 391;
                    when 22 => c := -416;
                    when 23 => c := -746;
                    when 24 => c := -701;
                    when 25 => c := -453;
                    when 26 => c := -174;
                    when 27 => c := 27;
                    when 28 => c := 117;
                    when 29 => c := 120;
                    when 30 => c := 82;
                    when 31 => c := 40;
                    when others => c := 7;
                end case;
                sop := to_integer(to_signed(sop, 2) + (taps(ii) * c));
            end loop;
            sig_out <= to_signed(shift_right(sop, 15), 16);
        end if;
    end if;
end process FIRFILT_HDL_SOP;

end architecture MyHDL;