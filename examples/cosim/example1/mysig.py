
import myhdl
from myhdl import instance, delay

class Clock(myhdl.SignalType):    
    def __init__(self, val, frequency=1):
        self._frequency = frequency
        myhdl.SignalType.__init__(self, bool(val))
        
    def _get_freq(self):
        return self._frequency
    def _set_freq(self, f):
        self.frequency = f
    frequency = property(_get_freq, _get_freq)

    def gen(self, hticks=2):
        self.hticks = hticks
        @instance
        def _clock():
            self.next = False
            while True:
                yield delay(hticks)
                self.next = not self.val
        return _clock

class Reset(myhdl.ResetSignal):
    def __init__(self, val, active, async):
        myhdl.ResetSignal.__init__(self,val,active,async)

    def pulse(self, delays=10):
        if isinstance(delays,(int,long)):
            self.next = self.active
            yield delay(delays)
            self.next = not self.active
        elif isinstance(delays,tuple):
            assert len(delays) in (1,2,3), "Incorrect number of delays"
            self.next = not self.active if len(delays)==3 else self.active
            for dd in delays:
                yield delay(dd)
                self.next = not self.val
        else:
            raise ValueError("%s type not supported"%(type(d)))
        
            


