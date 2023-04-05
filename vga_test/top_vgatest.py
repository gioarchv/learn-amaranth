from amaranth import *
from amaranth.build import Platform
from amaranth.sim import *
from vga import VGA
from tpg import TPG


class TopVgaTest(Elaboratable):
    def __init__(self) -> None:
        pass
    
    
    def elaborate(self, platform: Platform):
        m = Module()


        # vga signal generator
        m.submodules.vga = vga = VGA()    

        # vga signal definitions
        vga_hsync   = Signal()
        vga_vsync   = Signal()
        vga_de      = Signal()
        vga_frame   = Signal()
        vga_line    = Signal()
        vga_sx      = Signal(signed(16))
        vga_sy      = Signal(signed(16))

        m.d.comb += [
            vga_hsync.eq(vga.o_hsync),
            vga_vsync.eq(vga.o_vsync),
            vga_de.eq(vga.o_de),
            vga_frame.eq(vga.o_frame),
            vga_line.eq(vga.o_line),
            vga_sx.eq(vga.o_sx),
            vga_sy.eq(vga.o_sy),
        ]


        # vga test pattern generator
        m.submodules.tpg = tpg = TPG()

        # tpg signal definitions
        vga_r = Signal(4)
        vga_g = Signal(4)
        vga_b = Signal(4)

        m.d.comb += [
            tpg.i_sx.eq(vga_sx),
            tpg.i_sy.eq(vga_sy),
            vga_r.eq(tpg.o_r),
            vga_g.eq(tpg.o_g),
            vga_b.eq(tpg.o_b),
        ]

        return m


if __name__ == "__main__":
    dut = Module()
    dut.submodules.TopVgaTest = TopVgaTest = TopVgaTest()
    
    sim = Simulator(dut)
    sim.add_clock(25e-6)

    def process():
        for i in range(600000):
            yield Tick()

    sim.add_sync_process(process)
    with sim.write_vcd("top_vgatest.vcd", "top_vgatest.gtkw"):
        sim.run()