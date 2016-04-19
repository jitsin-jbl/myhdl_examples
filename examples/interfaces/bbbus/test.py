
from myhdl import *
from design import m_simple

def test():
    clock = Signal(bool(0))
    reset = ResetSignal(0, active=True, async=False)
    buttons = Signal(intbv(0)[5:])
    leds = Signal(intbv(0)[8:])

    def _test():
        tbdut = m_design_top(clock, reset, buttons, leds)

        @always(delay(3))
        def tbclk():
            clock.next = not clock

        @instance
        def tbstim():
            reset.next = reset.active
            yield delay(10)
            reset.next = not reset.active
            yield delay(10)

            buttons.next = 1
            for _ in range(8):
                yield clock.posedge
            assert leds == 0xFF
            buttons.next = 0

            yield delay(10)
            buttons.next = 0x1F
            yield clock.posedge
            buttons.next = 0
            for _ in range(8):
                yield clock.posedge
            assert leds == 0

            print("*** TEST PASSED ***")
            raise StopSimulation

        return tbdut, tbclk, tbstim

    Simulation(traceSignals(_test)).run()
    # MyHDL 0.9 supports conversions of interfaces, get the 
    # pre-release of 0.9 here: https://bitbucket.org/jandecaluwe/myhdl
    toVerilog(m_design_top, clock, reset, buttons, leds)
    toVHDL(m_design_top, clock, reset, buttons, leds)    
            
test()
