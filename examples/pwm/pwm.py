
import math
from myhdl import *

def m_pwm(
    # ~~~[Ports]~~~
    clock,             # system synchronous clock
    reset,             # system reset
    x,                 # signal input, signal to be modulated
    y,                 # PWM signal
    ts,                # The PWM sample rate, internally generated
    
    # ~~~[Parameters]~~~
    pwm_frequency=1e3, # desired PWM frequency
    ):
    """Genrated a PWM signal
        
    This module will generate a pulse width modulated signal (y).  This
    module will modulate the duty cycle of a square save.  The period
    (frequency) of the PWM is defined by the parameter *Fpwm*.
    
      Inputs
      ------
        clock : system clock
        reset : system reset
        x : multi-bit signal to be converted to PWM
        
      Outputs
      -------
        y : PWM signal
        ts : PWM sample rate strobe
        
      Parameters
      ----------
        pwm_frequency : PWM frequency (1/period)    
    """
    
    # Need to figure out how often to create our "strobe". The strobe
    # is the period of the PWM signal times x.max (i.e. how much we
    # are breaking up the PWM).  
    # The design will end up using two counters.
    Tmax = int(round(clock.frequency/pwm_frequency))
    Fact = clock.frequency / Tmax
    nbits = int(math.log(Tmax,2))
    nbits = nbits if nbits < len(x) else len(x)
    _tmax = Tmax
    Tmax = 2**nbits
    
    tcnt = Signal(intbv(0, min=0, max=Tmax))
    xu = Signal(intbv(Tmax/2, min=0, max=Tmax))

    # Adjust the input to be unsigned and truncate to the required
    # number of bits.
    Offset = abs(x.min)
    Shift = len(x) - nbits if len(x) > nbits else 0

    # Print out a summary of this module    
    print('   ~~~[PWM Module]~~~')
    print('    clock frequency ................... %.3f MHz' % (clock.frequency/1e6))
    print('    pwm frequency ..................... %.3f kHz' % (pwm_frequency/1e3))
    print('    local counter max ................. %d' % (Tmax))
    print('    pwm number of bits ................ %d' % (nbits))
    print('    pwm offset ........................ %d' % (Offset))
    print('    pwm shift ......................... %d' % (Shift))
    print('')
    
    # ~~~~[Logic to create the PWM signal]~~~~
    @always_seq(clock.posedge, reset=reset)
    def hdl_s2u():
        # most negative 0% duty, max positive ~100% duty
        if ts:
            xu.next = (x + Offset) >> Shift
                    
    @always_seq(clock.posedge, reset=reset)
    def hdl_pwm():
        if tcnt == Tmax-1:
            tcnt.next = 0
            ts.next = True
            y.next = 1
        else:
            tcnt.next = tcnt + 1
            ts.next = False
            if tcnt >= xu:
                y.next = 0

        
    return hdl_s2u, hdl_pwm
