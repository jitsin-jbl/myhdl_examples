-- File: test.vhd
-- Generated by MyHDL 0.9dev
-- Date: Sun Nov 24 21:18:19 2013


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_09.all;

entity test is
end entity test;


architecture MyHDL of test is


constant max: integer := 8;
constant min: integer := -8;



signal a: signed (3 downto 0);
signal q3: signed (5 downto 0);
signal q2: signed (5 downto 0);
signal clock: std_logic;
signal b: signed (3 downto 0);
signal mode: std_logic;

begin




TEST_TB_DUT_RTL: process (clock) is
    variable q1: signed(5 downto 0);
begin
    if rising_edge(clock) then
        if bool(mode) then
            q1 := (resize(a, 6) + b);
        else
            q1 := (resize(a, 6) - b);
        end if;
        q2 <= (q1 + shift_right(q2, 2));
    end if;
end process TEST_TB_DUT_RTL;


TEST_TB_DUT_RTL_PIPED: process (clock) is
    variable q1: signed(5 downto 0);
begin
    if rising_edge(clock) then
        q3 <= (q1 + shift_right(q2, 2));
    end if;
end process TEST_TB_DUT_RTL_PIPED;


TEST_TB_CLK: process is
begin
    clock <= '0';
    while True loop
        wait for 3 ns;
        clock <= stdl((not bool(clock)));
    end loop;
    wait;
end process TEST_TB_CLK;


TEST_TB_STIM: process is
begin
    for mm in 0 to 2-1 loop
        mode <= stdl(mm);
        for aa in min to max-1 loop
            for bb in min to max-1 loop
                a <= to_signed(aa, 4);
                b <= to_signed(bb, 4);
                wait until rising_edge(clock);
                for ii in 0 to 5-1 loop
                    wait until rising_edge(clock);
                    assert (q3 = q2)
                        report "*** AssertionError ***"
                        severity error;
                end loop;
            end loop;
        end loop;
    end loop;
    assert False report "End of Simulation" severity Failure;
    wait;
end process TEST_TB_STIM;

end architecture MyHDL;
