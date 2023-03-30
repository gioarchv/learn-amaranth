from amaranth import *
from amaranth.build import *

import sys
sys.path.insert(0,"..")
from boards.alchitry_cu import AlchitryCuPlatform

class Blink(Elaboratable):

    def elaborate(self, platform: Platform) -> Module:
        m = Module()

        led = platform.request("led")

        half_freq = int(platform.default_clk_frequency // 2)
        timer = Signal(range(half_freq + 1))

        with m.If(timer == half_freq):
            m.d.sync += led.eq(~led)
            m.d.sync += timer.eq(0)
        with m.Else():
            m.d.sync += timer.eq(timer + 1)

        return m



if __name__ == "__main__":
    AlchitryCuPlatform().build(Blink(), do_program=False)

        