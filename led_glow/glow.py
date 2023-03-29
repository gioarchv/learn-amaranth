from nmigen import *
from nmigen.build import *
from nmigen.build.run import LocalBuildProducts
from nmigen.vendor.lattice_ice40 import LatticeICE40Platform

from boards.alchitry_cu import AlchitryCuPlatform


class Glow(Elaboratable):

    def elaborate(self, platform: Platform) -> Module:
        m = Module()

        leds = platform.request("led")

        half_freq = int(platform.default_clk_frequency // 2)
        timer = Signal(range(half_freq + 1))
        count = Signal(8)

        with m.If(timer == half_freq):
            m.d.sync += count.eq(count + 1)
            m.d.sync += timer.eq(0)
        with m.Else():
            m.d.sync += timer.eq(timer + 1)

        m.d.comb += leds.eq(count)

        return m



if __name__ == "__main__":
    AlchitryCuPlatform().build(Glow(), do_program=False)


        