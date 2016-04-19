#
# Copyright (c) 2011 Christopher Felton
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
#


"""
============================
Example modbv Test Suite
============================

"""

from myhdl import *
from random import randint
from rrs_modbv import rrs_modbv
from time import time

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# globally define signals and generators used by all tests
D     = 16
Nbits = 16
Max = 2**(Nbits-1)
Min = -1*Max

clk = Signal(True)
rst = Signal(False)
x   = Signal(intbv(0, min=Min, max=Max))
y   = Signal(intbv(0, min=Min, max=Max))


@always(delay(4))
def tb_clk_gen():
    clk.next = not clk

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_positiveRange():

    def tbs():
        """Testbench function"""

        dut = example_modbv(clk, rst, x, y, D=D, Max=Max, Min=Min)
        
        @instance
        def tb_stimulus():
            rst.next = True
            yield delay(10)
            rst.next = False

            for rr in xrange(Max):
                yield clk.posedge
                for ii in xrange(2*D):
                    x.next = rr
                    yield clk.posedge
                    if ii >= (D):
                        assert y == rr, "Average of constant failed %d != %d" % (rr, y)

            raise StopSimulation

        return tb_stimulus, tb_clk_gen, dut

    tb = tbs()
    Simulation(tb).run()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_negativeRange():


    def tbs():
        """Testbench function"""
        
        dut = example_modbv(clk, rst, x, y, D=D, Max=Max, Min=Min)

        @instance
        def tb_stimulus():
            rst.next = True
            yield delay(10)
            rst.next = False

            for rr in xrange(0, Min, -1):
                yield clk.posedge
                for ii in xrange(2*D):
                    x.next = rr
                    yield clk.posedge
                    if ii >= (D):
                        assert y == rr, "Average of constant failed %d != %d" % (rr, y)

            raise StopSimulation

        return tb_stimulus, tb_clk_gen, dut


    tb = tbs()
    Simulation(tb).run()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_random():
    Ntests = 13
    Nloops = 212141*D

    def tbs():
        dut = example_modbv(clk, rst, x, y, D=D, Max=Max, Min=Min)
        
        @instance
        def tb_stimulus():
            rst.next = True
            yield delay(10)
            rst.next = False
        
            for nn in xrange(Ntests):
                bsum  = 0.
                for ii in xrange(Nloops):
                    rval = randint(Min, Max-1)
                    if ii % D == 0:
                        bsum = rval
                    else:
                        bsum = bsum + rval
                    x.next = rval
                    yield clk.posedge
        
                bavg = bsum/D
                assert bavg == y, 'Random test %d computed average %d filtered average %d ' % (nn, bavg, y)
                
            raise StopSimulation

        return tb_stimulus, tb_clk_gen, dut

    tb = tbs()
    Simulation(tb).run()
    


if __name__ == '__main__':
    start = time()
    test_positiveRange()
    test_negativeRange()
    test_random()
    print " %4.2f minutes" % ((time()-start)/60.)
