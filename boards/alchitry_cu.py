import os
import subprocess

from amaranth import *
from amaranth.build import *
from amaranth.build.run import LocalBuildProducts
from amaranth.vendor.lattice_ice40 import LatticeICE40Platform

__all__ = ["AlchitryCuPlatform"]

class AlchitryCuPlatform(LatticeICE40Platform):
    device      = "iCE40HX8K"
    package     = "CB132"
    default_clk = "clk100"
    default_rst = "rst"

    resources   = [
        Resource("clk100", 0, Pins("P7", dir="i"), Clock(10e7), 
                Attrs(GLOBAL=True, IO_STANDARD="SB_LVCMOS")),
        Resource("rst", 0, Pins("P8", dir="i", invert=True),
                Attrs(IO_STANDARD="SB_LVCMOS")),


        # On-Board LED Array
        Resource("led", 0, Pins("J11 K11 K12 K14 L12 L14 M12 N14", dir="o"),
                Attrs(IO_STANDARD="SB_LVCMOS")),

        Resource("uart", 0,
                Subsignal("tx", Pins("M9",  dir="o")),
                Subsignal("rx", Pins("P14", dir="i")),
                Attrs(IO_STANDARD="SB_LVCMOS")
        ),

        Resource("i2s", 0,
                Subsignal("lrck", Pins("N1",  dir="o")),        # Bank A Pin 48
                Subsignal("bck",  Pins("P1",  dir="o")),        # Bank A Pin 49
                Subsignal("din",  Pins("L1",  dir="o")),        # Bank A Pin 3
                Attrs(IO_STANDARD="SB_LVCMOS")
        ),
    ]

    
    connectors  = [
        Connector("bank A", 0, "M1  L1  J1  J3  G1  G3  E1  D1  C1  B1  D3  C3  A1  A2  A3  A4"
                               "P1  N1  K4  K3  H3  H1  G4  H4  F3  F4  E4  D4  C4  D5  C5  A5"),
        Connector("bank B", 1, "-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -"
                               "-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -"),
        Connector("bank C", 2, "-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -"
                               "-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -"),
        Connector("bank D", 3, "K12   K14   M12   N14   -   -   -   -   P14   M9   -   -   -   -   -   -"
                               "J11   K11   L12   L14   -   -   P7   P8   -   -   -   -   -   -   -   -")
    ]
    

    def toolchain_program(self, products: LocalBuildProducts, name: str):
        iceprog = os.environ.get("ICEPROG", "iceprog")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([iceprog, bitstream_filename])