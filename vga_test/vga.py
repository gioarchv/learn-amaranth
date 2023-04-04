from amaranth import *
from amaranth.build import Platform
from amaranth.sim import *


class VGA(Elaboratable):
    def __init__(self,
                 CORDW  = 16,
                 H_RES  = 800,
                 V_RES  = 480,
                 H_FP   = 40,
                 H_SYNC = 48,
                 H_BP   = 88,
                 V_FP   = 13,
                 V_SYNC = 3,
                 V_BP   = 32,
                 H_POL  = 0,
                 V_POL  = 0):
        # Ports
        #self.i_clk_pix  = Signal()
        #self.i_rst_pix  = Signal()
        self.o_hsync    = Signal()
        self.o_vsync    = Signal()
        self.o_de       = Signal()
        self.o_frame    = Signal()
        self.o_line     = Signal()
        self.o_sx       = Signal(signed(CORDW))
        self.o_sy       = Signal(signed(CORDW))

        # Configuration
        self.CORDW  = CORDW
        self.H_RES  = H_RES
        self.V_RES  = V_RES
        self.H_FP   = H_FP
        self.H_SYNC = H_SYNC
        self.H_BP   = H_BP
        self.V_FP   = V_FP
        self.V_SYNC = V_SYNC
        self.V_BP   = V_BP
        self.H_POL  = H_POL
        self.V_POL  = V_POL

    def ports(self):
        return [self.o_hsync,
                self.o_vsync,
                self.o_de,
                self.o_frame,
                self.o_line,
                self.o_sx,
                self.o_sy,
        ]
    
    def elaborate(self, platform: Platform) -> Module:
        m = Module()

        # Horizontal timings
        H_STA   = Const((0 - self.H_FP - self.H_SYNC - self.H_BP), signed(self.CORDW))
        HS_STA  = Const((0 - self.H_FP - self.H_SYNC - self.H_BP - self.H_FP), signed(self.CORDW))
        HS_END  = Const((0 - self.H_FP - self.H_SYNC - self.H_BP - self.H_FP + self.H_SYNC), signed(self.CORDW))
        HA_STA  = Const(0, signed(self.CORDW))
        HA_END  = Const((self.H_RES - 1), signed(self.CORDW))

        # Vertical timings
        V_STA   = Const((0 - self.V_FP - self.V_SYNC - self.V_BP), signed(self.CORDW))
        VS_STA  = Const((0 - self.V_FP - self.V_SYNC - self.V_BP - self.V_FP), signed(self.CORDW))
        VS_END  = Const((0 - self.V_FP - self.V_SYNC - self.V_BP - self.V_FP - self.V_SYNC), signed(self.CORDW))
        VA_STA  = Const(0, signed(self.CORDW))
        VA_END  = Const((self.V_RES - 1), signed(self.CORDW))


        # Internal signals
        R_x     = Signal(signed(self.CORDW), reset=0)
        R_y     = Signal(signed(self.CORDW), reset=0)
        R_hsync = Signal(reset=0)
        R_vsync = Signal(reset=0)
        R_de    = Signal(reset=0)
        R_frame = Signal(reset=0)
        R_line  = Signal(reset=0)

        # generate horizontal and vertical sync with correct polarity
        
        with m.If(ResetSignal()):
            m.d.sync += [
                R_hsync.eq(Mux(self.H_POL, 0, 1)),
                R_vsync.eq(Mux(self.H_POL, 0, 1)),
            ]
        with m.Else():
            m.d.sync += [
            R_hsync.eq(Mux(self.H_POL, ((R_x > HS_STA) & (R_x <= HS_END)), ~((R_x > HS_STA) & (R_x <= HS_END)))),
            R_vsync.eq(Mux(self.V_POL, ((R_y > VS_STA) & (R_y <= VS_END)), ~((R_y > VS_STA) & (R_y <= VS_END)))),
            ]


       # Control signals
        m.d.sync += [
            R_de.eq((R_y > VA_STA) & (R_x >= HA_STA)),
            R_frame.eq((R_y == V_STA) & (R_x == H_STA)),
            R_line.eq(R_x == H_STA),
        ]

        # Calculate horizontal and vertical screen position
        with m.If(ResetSignal()):
            m.d.sync += [
                R_x.eq(H_STA),
                R_y.eq(V_STA),
            ]
        with m.Elif(R_x == HA_END):
            m.d.sync += [
                R_x.eq(H_STA),
                R_y.eq(Mux((R_y == VA_END), V_STA, R_y + 1)),
            ]
        with m.Else():
            m.d.sync += [
                R_x.eq(R_x + 1)
            ]


        # delay screen position to match sync and control signals
        with m.If(ResetSignal()):
            m.d.sync += [
                self.o_sx.eq(H_STA),
                self.o_sy.eq(V_STA),
            ]
        with m.Else():
            m.d.sync += [
            self.o_sx.eq(R_x),
            self.o_sy.eq(R_y),
            ]



        # outputs
        m.d.comb += [
        self.o_hsync.eq(R_hsync),
        self.o_vsync.eq(R_vsync),
        self.o_de.eq(R_de),
        self.o_frame.eq(R_frame),
        self.o_line.eq(R_line),
        ]


        return m


if __name__ == "__main__":
    dut = Module()
    dut.submodules.vga = vga = vga()

    sim = Simulator(dut)
    sim.add_clock(25e-6)


    def process():
        for i in range(600000):
            yield Tick()

    sim.add_sync_process(process)
    with sim.write_vcd("vga.vcd", "vga.gtkw", traces=vga.ports()):
        sim.run()