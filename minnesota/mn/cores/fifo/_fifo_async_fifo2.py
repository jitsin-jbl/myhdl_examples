
#
# Copyright (c) 2006-2014 Christopher L. Felton
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

from math import log, ceil

from myhdl import *

from _fifo_mem import m_fifo_mem_generic
from _fifo_intf import check_fifo_intf
from _fifo_intf import _fifobus

def m_fifo_async(reset, wclk, rclk, fbus):
    """
    The following is a general purpose, platform independent 
    asynchronous FIFO (dual clock domains).

    Cross-clock boundrary FIFO, based on: 
    ~~"Simulation and Synthesis Techniques for Asynchronous FIFO 
    Design with Asynchronous Pointer Comparisons"~~
    "Simulation and Synthesis Techniques for Asynchronous FIFO Design"
    """
    check_fifo_intf(fbus)

    # for simplification the memory size is force to a power of 
    # two - full address range, ptr (mem indexes) will wrap
    Asz = int(ceil(log(fbus.size, 2)))
    Dsz = len(fbus.wdata)
    MMax = 2**Asz
    
    wptr = Signal(intbv(0)[Asz:])
    rptr = Signal(intbv(0)[Asz:])

    wfull = Signal(bool(0))
    afull_n  = Signal(bool(1))
    rempty = Signal(bool(1))
    aempty_n = Signal(bool(0))
    p_aempty_n = Signal(bool(0))

    wrst_n = Signal(bool(0))
    rrst_n = Signal(bool(0))

    # @todo: reset syncronizers
    wrst_s = [Signal(bool(0)) for ii in range(2)]
    rrst_s = [Signal(bool(0)) for ii in range(2)]

    @always_comb
    def rtl_assigns():
        fbus.empty.next = rempty
        fbus.full.next = wfull

    # @todo: if ResetSignal use the active attribute to determine 
    #        if 'not reset' or 'reset'
    @always(wclk.posedge)
    def rtl_wreset_s():
        wrst_s[0].next = not reset
        wrst_s[1].next = wrst_s[0]

    @always(rclk.posedge)
    def rtl_rreset_s():
        rrst_s[0].next = not reset
        rrst_s[1].next = rrst_s[0]

    @always_comb
    def rtl_resets():
        wrst_n.next = wrst_s[1]
        rrst_n.next = rrst_s[1]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # --Text from the paper--
    # This is an asynchronous pointer-comparison module that
    # is used to generate signals that control assertions of the
    # asynchronous "full" and "empty" status bits.  This module
    # only contains combinational comparison logic.  No sequential
    # logic is included.
    direction = Signal(False)
    dirset_n  = Signal(False)
    dirclr_n  = Signal(False)
    high      = Signal(True)

    wrm  = Signal(False)
    wrl = Signal(False)
    
    N = Asz-1
    
    # generate the quadrant changes
    @always_comb
    def rtl_async_quad():
        wrm.next = wptr[N] ^ rptr[N-1]
        wrl.next = wptr[N-1] ^ rptr[N]

    @always_comb
    def rtl_async_cmp_dir():
        high.next = True
        if wrm and not wrl:
            dirset_n.next = False
        else:
            dirset_n.next = True

        if (not wrm and wrl) or not wrst_n:
            dirclr_n.next = False
        else:
            dirclr_n.next = True

        if (wptr-1) == rptr and not direction:
            p_aempty_n.next = False
        else:
            p_aempty_n.next = True

        if (wptr == rptr) and not direction:
            aempty_n.next = False
        else:
            aempty_n.next = True            

        if (wptr == rptr) and direction:
            afull_n.next = False
        else:
            afull_n.next = True


    # desired RS-FF (might look odd, generates the desired)
    @always(wclk.posedge, dirset_n.negedge, dirclr_n.negedge)
    def rtl_async_cmp():
        if not dirclr_n:
            direction.next = False
        elif not dirset_n:
            direction.next = True
        else:
            if not high:
                direction.next = high

    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Memory for the FIFO
    g_fifomem = m_fifo_mem_generic(wclk, fbus.wr, fbus.wdata, wptr,
                                   rclk, fbus.rdata,  rptr,
                                   mem_size=fbus.size)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # --Text from the paper--
    # This module is mostly synchronous to the read-clock.
    # domain and contains the FIFO read pointer and empty-flag
    # logic.  Assertion of the aempty_n signal (an input to 
    # this module) is synchronous to the rclk-domain, since aempty_n 
    # can only be asserted when the rptr incremented, but de-assertion
    # of the aempty_n signal happens when the wptr increments, which
    # is asynchronous to rclk.
    rbin    = Signal(intbv(0)[Asz:])
    rgnext  = Signal(intbv(0)[Asz:])
    rbnext  = Signal(intbv(0)[Asz:])
    rempty2 = Signal(False)
    
    # gray style pointer
    @always(rclk.posedge, rrst_n.negedge)
    def rtl_rptr_bin():
        if not rrst_n:
            rbin.next = 0
            rptr.next = 0
        else:
            rbin.next = rbnext
            rptr.next = rgnext

    @always_comb
    def rtl_rptr_inc():
        if not rempty and fbus.rd:
            rbnext.next = (rbin + 1) % MMax
        else:
            rbnext.next = rbin

    @always_comb
    def rtl_rptr_gray():
        # binary-to-gray conversion
        rgnext.next = (rbnext>>1) ^ rbnext

    @always(rclk.posedge, aempty_n.negedge)
    def rtl_rptr_empty():
        if not aempty_n:
            rempty.next  = True
            rempty2.next = True
        else:
            rempty2.next = not aempty_n
            rempty.next  = rempty2

    _rvld1  = Signal(False)
    _rempty = Signal(False)

    @always(rclk.posedge)
    def rtl_rd_vld():
        _rvld1.next  =  fbus.rd
        _rempty.next = rempty;
        
    @always_comb
    def rtl_rd_vldo():
        fbus.rvld.next = _rvld1 and not _rempty
    

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # --Text from the paper--
    # This module is mostly synchronous to the write-clock domain
    # and contains the FIFO write pointer and full-flag logic.  Assertion
    # of the afull_n signal (an input to this module) is syncronous to
    # the wclk domain, since afull_n can only be asserted when the 
    # wptr incremented (and wrst_n), but deassertion of the afull_n 
    # signal happens when the rptr increments, whichis asynchronous to wclk.
    wbin   = Signal(intbv(0)[Asz:])
    wgnext = Signal(intbv(0)[Asz:])
    wbnext = Signal(intbv(0)[Asz:])
    wfull2 = Signal(False)

    @always(wclk.posedge, wrst_n.negedge)
    def rtl_wptr_bin():
        if not wrst_n :
            wbin.next = 0
            wptr.next = 0
        else:
            wbin.next = wbnext
            wptr.next = wgnext

    @always_comb
    def rtl_wptr_inc():
        if not wfull and fbus.wr:
            wbnext.next = (wbin + 1) % MMax
        else:
            wbnext.next = wbin

    @always_comb
    def rtl_wptr_gray():
        wgnext.next = (wbnext>>1) ^ wbnext

    @always(wclk.posedge, wrst_n.negedge, afull_n.negedge)
    def rtl_wptr_full():
        if not wrst_n:
            wfull.next  = False
            wfull2.next = False
        elif not afull_n:
            wfull.next  = True
            wfull2.next = True
        else:
            wfull.next  = wfull2
            wfull2.next = not afull_n


    return instances()
    #(rtl_wreset_s, rtl_rreset_s, rtl_resets, rtl_async_quad,
    #        rtl_async_cmp_dir, rtl_async_comp, rtl_rptr_bin, rtl_rptr_inc,
    #        rtl_rptr_gray, rtl_rptr_empty, rtl_rd_vld, rtl_rd_vldo, 
    #        rtl_wptr_bin, rtl_wptr_inc, rtl_wptr_gray, rtl_wptr_full)

m_fifo_async.fbus_intf = _fifobus