-- File: m_think.vhd
-- Generated by MyHDL 0.8
-- Date: Fri Sep  6 14:16:54 2013


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_08.all;

entity m_think is
    port (
        clock: in std_logic;
        reset: in std_logic;
        thinking: out std_logic;
        sending: out std_logic;
        sent: out unsigned(43 downto 0)
    );
end entity m_think;


architecture MyHDL of m_think is




type t_enum_states_1 is (
    IDLE,
    THINK,
    SEND_CMD,
    ADVANCE
);
attribute enum_encoding of t_enum_states_1: type is "0001 0010 0100 1000";

signal state: t_enum_states_1;
signal lsent: unsigned(43 downto 0);

begin




M_THINK_RTL: process (clock, reset) is
begin
    if (reset = '0') then
        thinking <= '0';
        sending <= '0';
        state <= IDLE;
        lsent <= to_unsigned(0, 44);
    elsif rising_edge(clock) then
        thinking <= '0';
        sending <= '0';
        case state is
            when IDLE =>
                state <= THINK;
            when THINK =>
                thinking <= '1';
                state <= SEND_CMD;
            when SEND_CMD =>
                sending <= '1';
                state <= ADVANCE;
            when ADVANCE =>
                lsent <= (lsent + 1);
                state <= IDLE;
            when others =>
                assert False
                    report "*** AssertionError ***"
                    severity error;
        end case;
    end if;
end process M_THINK_RTL;

end architecture MyHDL;
