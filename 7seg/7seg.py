from amaranth import *
from amaranth.build import *

import sys
sys.path.insert(0,"..")
from boards.alchitry_cu import AlchitryCuPlatform

seven_seg_io = [
    Resource("seven_seg", 0,
             Subsignal("aa", PinsN("J1", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("ab", PinsN("J3", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("ac", PinsN("N1", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("ad", PinsN("K4", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("ae", PinsN("K3", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("af", PinsN("L1", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("ag", PinsN("M1", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("d0", PinsN("G3", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("d1", PinsN("G1", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("d2", PinsN("H1", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("d3", PinsN("H3", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")))
]


class Top(Elaboratable):
    def __init__(self):
        # TODO: Figure out how to expose the P1A{1-4, 7-10} pins in the
        # constructor so Top can be built in a potentially platform-agnostic
        # way using amaranth.cli.main. For now, only put child modules in
        # constructor.
        self.ones_to_segs = DigitToSegments()
        self.tens_to_segs = DigitToSegments()
        self.hund_to_segs = DigitToSegments()
        self.thou_to_segs = DigitToSegments()


    def elaborate(self, platform):
        seg_pins = platform.request("seven_seg")

        m = Module()

        seg_pins_cat = Signal(7)

        counter = Signal(42)
        ones_counter = Signal(4)
        tens_counter = Signal(4)
        hund_counter = Signal(4)
        thou_counter = Signal(4)
        display_state = Signal(4)
        multiplex = Signal(4)

        m.submodules.ones_to_segs = self.ones_to_segs
        m.submodules.tens_to_segs = self.tens_to_segs
        m.submodules.hund_to_segments = self.hund_to_segs
        m.submodules.thou_to_segments = self.thou_to_segs

        m.d.comb += [
            Cat([seg_pins.aa, seg_pins.ab, seg_pins.ac, seg_pins.ad,
                 seg_pins.ae, seg_pins.af, seg_pins.ag]).eq(seg_pins_cat),
            Cat([seg_pins.d3, seg_pins.d2, seg_pins.d1, seg_pins.d0]).eq(multiplex),
            ones_counter.eq(counter[25:29]),
            tens_counter.eq(counter[29:33]),
            hund_counter.eq(counter[33:37]),
            thou_counter.eq(counter[37:41]),
            display_state.eq(counter[13:17]),
            self.ones_to_segs.digit.eq(ones_counter),
            self.tens_to_segs.digit.eq(tens_counter),
            self.hund_to_segs.digit.eq(hund_counter),
            self.thou_to_segs.digit.eq(thou_counter)
        ]

        m.d.sync += counter.eq(counter + 1)

        with m.Switch(display_state):
            with m.Case("0000"):
                m.d.sync += seg_pins_cat.eq(self.ones_to_segs.segments)
            with m.Case("0010"):
                m.d.sync += seg_pins_cat.eq(0)
            with m.Case("0011"):
                m.d.sync += multiplex.eq(0b0100)
            with m.Case("0100"):
                m.d.sync += seg_pins_cat.eq(self.tens_to_segs.segments)
            with m.Case("0110"):
                m.d.sync += seg_pins_cat.eq(0)
            with m.Case("0111"):
                m.d.sync += multiplex.eq(0b0010)
            with m.Case("1000"):
                m.d.sync += seg_pins_cat.eq(self.hund_to_segs.segments)
            with m.Case("1010"):
                m.d.sync += seg_pins_cat.eq(0)
            with m.Case("1011"):
                m.d.sync += multiplex.eq(0b0001)
            with m.Case("1100"):
                m.d.sync += seg_pins_cat.eq(self.thou_to_segs.segments)
            with m.Case("1110"):
                m.d.sync += seg_pins_cat.eq(0)
            with m.Case("1111"):
                m.d.sync += multiplex.eq(0b1000)
            

        return m


class DigitToSegments(Elaboratable):
    def __init__(self) -> None:
        self.digit = Signal(4)
        self.segments = Signal(7)

    def elaborate(self, _platform):
        m = Module()

        with m.Switch(self.digit):
            for n, seg_val in enumerate([
                0b0111111,
                0b0000110,
                0b1011011,
                0b1001111,
                0b1100110,
                0b1101101,
                0b1111101,
                0b0000111,
                0b1111111,
                0b1101111,
                0b1110111,
                0b1111100,
                0b0111001,
                0b1011110,
                0b1111001,
                0b1110001]):
                with m.Case(n):
                    m.d.sync += self.segments.eq(seg_val)

        return m
    

if __name__ == "__main__":
    # In this example, explicitly show the intermediate classes used to
    # execute build() to demonstrate that a user can inspect
    # each part of the build process (create files, execute, program,
    # and create a zip file if you have a BuildPlan instance).
    plat = AlchitryCuPlatform()
    plat.add_resources(seven_seg_io)

    # BuildPlan if do_build=False
    # BuildProducts if do_build=True and do_program=False
    # None otherwise.
    plan = plat.build(Top(), do_build=False, do_program=False)  # BuildPlan
    products = plan.execute()  # BuildProducts
    plat.toolchain_program(products, "top")  # Manally run the programmer.

