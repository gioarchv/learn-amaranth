from amaranth import *
from amaranth.cli import main

class Blinker(Elaboratable):
    def __init__(self, period) -> None:
        assert period % 2 == 0, 'period must be even'
        self.period = period
        self.led = Signal()
        self.counter = Signal((period - 4).bit_length())
        self.ports = [self.led]

    
    def elaborate (self, platform):
        m = Module()

        with m.If(self.counter[-1]):
            m.d.sync += [
                self.counter.eq(self.period // 2 -2),
                self.led.eq(~self.led),
            ]
        with m.Else():
            m.d.sync += [
                self.counter.eq(self.counter - 1),
            ]

        return m
    

if __name__== '__main__':
    top = Blinker(period=100)
    main(top, ports=top.ports)