
# Copyright (c) 2014 Christopher L. Felton
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from myhdl import *

from _fifo_intf import check_fifo_intf
from _fifo_intf import _fifobus

def m_fifo_sync(reset, clock, fbus, fast=True, use_srl_prim=False):
    """
    Often small simple, synchronous, FIFOs can be implemented with 
    specialized hardware in an FPGA (e.g. vertically chaining LUTs).

    This FIFO is intended to be used for small fast FIFOs.  But when
    used for large 
    
    This FIFO is a small FIFO (currently fixed to 16) that is implemented
    to take advantage of some hardware implementations.

    Typical FPGA synthesis will infer shift-register-LUT (SRL) for small
    synchronous FIFOs.  This FIFO is implemented generically, consult the
    synthesis and map reports.

    PORTS
    =====

    PARAMETERS
    ==========
    fast : this indicates the FIFO is intended to be used as a fast
      (small/short) FIFO.

    use_slr_prim: this parameter indicates to use the SRL primitive
      (inferrable primitive).  If SRL are not inferred from the generic
      description this option can be used.  Note, srl_prim will only
      use a size (FIFO depth) of 16.
    """

    # @todo: this is intended to be used for small fast fifo's but it
    #        can be used for large synchronous fifo as well
    W = 16   # default and max size    
    if use_srl_prim:
        W = 16
    elif fast and fbus.size > W:
        print("@W: m_fifo_short only supports size < %d, for fast" % (W))
        print("    forcing size (depth) to %d" % (W))    
    else:
        W = fbus.size

    mem = [Signal(intbv(0)[fbus.width:]) for _ in range(W)]
    addr = Signal(intbv(0, min=0, max=W))

    srlce = fbus.wr     # single cycle write
    fbus.rvld = rd      # no delay on reads
    
    # typically this should be implemented with SRL if available, or
    # use the finer SRL description: 
    #    gsrl = [None for _ in range(W)]
    #    for ii in range(W):
    #       gsrl[ii] = m_fifo_srl(clock, fbus.wdata[ii], fbus.wr, 
    #                             addr, fbus.rdata[ii])
    # note: signal slices wdata() will need to be used instead of
    #       bit slices wsdata[].  Have add 

    @always(clock.posedge)
    def rtl_srl_in():
        if srlce:
            mem[addr].next = fbus.wdata

    @always_comb
    def rtl_srl_out():
        fbus.rdata.next = mem[W-1]

    @always_comb
    def rtl_vld():
        fbus.rvld.next = fbus.rd    # no delay on reads

    @always_seq(clock.posedge, reset=reset)
    def rtl_fifo():
        if fbus.clear:
            addr.next = 0
            fbus.empty.next = True
            fbus.full.next = False

        elif fbus.rd and not fbus.wr:
            fbus.full.next = False
            if addr == 0:
                fbus.empty.next = True
            addr.next = addr - 1

        elif fbus.wr and not fbus.rd:
            fbus.empty.next = False
            if not fbus.empty:
                addr.next = addr + 1
            if addr == W-2:
                fbus.full.next = True

        # nothing happens if read and write at the same time
            
    # note: failures occur if write/read when full/empty respectively
                
    nvacant = Signal(intbv(0, min=0, max=W+1))  # # empty slots
    ntenant = Signal(intbv(0, min=0, max=W+1))  # # filled slots

    @always_seq(clock.posedge, reset=reset)
    def dbg_occupancy():
        if clear:
            nvacant.next = W
            ntenant.next = 0
        elif fbus.rd and not fbus.wr:
            nvacant.next = space + 1
            ntenant.next = space - 1
        elif fbus.wr and not fbus.rd:
            nvacant.next = space - 1
            ntenant.next = space + 1

    return rtl_srl_in, rtl_srl_out, rtl_vld, rtl_fifo, dbg_occupancy