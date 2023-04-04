from amaranth import *
from amaranth.build import *

import sys
sys.path.insert(0,"..")
from boards.alchitry_cu import AlchitryCuPlatform
from lib.pll import PLL
from blink.blinker import Blinker


class Top(Elaboratable):
    def elaborate(self, platform):
        # If you don't specify dir='-', you will experience a world
        # of debugging pain.
        clk_pin = platform.request(platform.default_clk, dir='-')
        leds = platform.request('led', 0)
        #led1 = platform.request('led', 1)
        freq_in = platform.default_clk_frequency
        pll_freq = 25_000_000
        freq_in_mhz = freq_in / 1_000_000
        pll_freq_mhz = pll_freq / 1_000_000
        bink0_period = int(pll_freq)
        bink1_period = pll_freq // 5

        m = Module()
        pll = PLL(freq_in_mhz=freq_in_mhz, freq_out_mhz=pll_freq_mhz)
        bink0 = Blinker(period=bink0_period)
        bink1 = Blinker(period=bink1_period)
        m.domains += pll.domain     # override the default 'sync' domain
        m.submodules += [pll, bink0, bink1]
        m.d.comb += [
            pll.clk_pin.eq(clk_pin),
            leds.eq(Cat(bink0.led, Repl(0,6), bink1.led)),
        ]
        return m


if __name__ == '__main__':
    platform = AlchitryCuPlatform()
    platform.build(Top(), do_program=True)
    