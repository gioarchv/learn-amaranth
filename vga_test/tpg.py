from amaranth import *
from amaranth.build import Platform
from amaranth.sim import *

class TPG(Elaboratable):
    def __init__(self,
                 CORDW = 16,
                 ):
        self.i_sx = Signal(signed(CORDW))
        self.i_sy = Signal(signed(CORDW))
        self.o_r = Signal(4)
        self.o_g = Signal(4)
        self.o_b = Signal(4)

    def ports(self):
        return [self.i_sx,
                self.i_sy,
                self.o_r,
                self.o_g,
                self.o_b,
                ]       

    def elaborate(self, platform: Platform) -> Module:
        m = Module()

        """
        Color Bars pattern
        Divides active area into 8 equal bars and colours them
        according to this truth table:
        R   G   B   bar_select  output color
        0   0   0       0           Black
        0   0   1       1           Blue
        0   1   0       2           Green
        0   1   1       3           Turquoise
        1   0   0       4           Red
        1   0   1       5           Purple
        1   1   0       6           Yellow
        1   1   1       7           White
        """

        # Constants
        ACTIVE_COLS = 800
        VIDEO_WIDTH = 4
        BAR_WIDTH = ACTIVE_COLS // 8

        # Internal Signals
        bar_select = Signal(3)

        m.d.comb += [ 
            bar_select.eq(Mux((self.i_sx < (BAR_WIDTH * 1)), 0,
                          (Mux((self.i_sx < (BAR_WIDTH * 2)), 1,
                          (Mux((self.i_sx < (BAR_WIDTH * 3)), 2,
                          (Mux((self.i_sx < (BAR_WIDTH * 4)), 3,
                          (Mux((self.i_sx < (BAR_WIDTH * 5)), 4,
                          (Mux((self.i_sx < (BAR_WIDTH * 6)), 5,
                          (Mux((self.i_sx < (BAR_WIDTH * 7)), 6, 7)))))))))))))),

            self.o_r.eq(Mux(((bar_select == 4) | (bar_select == 5) | 
                            (bar_select == 6) | (bar_select == 7)), 
                            Repl(1, VIDEO_WIDTH), 0)),

            self.o_g.eq(Mux(((bar_select == 2) | (bar_select == 3) | 
                            (bar_select == 6) | (bar_select == 7)), 
                            Repl(1, VIDEO_WIDTH), 0)),

            self.o_b.eq(Mux(((bar_select == 1) | (bar_select == 3) | 
                            (bar_select == 5) | (bar_select == 7)), 
                            Repl(1, VIDEO_WIDTH), 0)),
        ]

        return m 
    

    if __name__ == "__main__":
        dut = Module()
        dut.submodules.tpg = tpg = tpg()
        
        sim = Simulator(dut)
        sim.add_clock(25e-6)

        def process():
            for i in range (600000):
                yield Tick()

        sim.add_sync_process(process)
        with sim.write_vcd("tpg.vcd", "tpg.gtkw", traces=tpg.ports()):
            sim.run()