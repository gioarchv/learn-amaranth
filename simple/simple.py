from nmigen import *
from nmigen.back.pysim import *

class SimpleModule (Elaboratable):
    def __init__(self) -> None:
        self.count = Signal( 16, reset = 0)
        self.ncount = Signal( 16, reset = 0)

    def ports(self):
        return [self.count, self.ncount]
    
    def elaborate (self, platform):
        m = Module()
        m.d.comb += self.ncount.eq( ~self.count )
        m.d.sync += self.count.eq( self.count + 1 )
        return m

if __name__=="__main__":
    m = Module()
    m.submodules.simple = simple = SimpleModule()
    m.domains.sync = sync = ClockDomain("sync", async_reset=True)
    
    sim = Simulator(m)
    sim.add_clock(1e-6)


    def process():
        for i in range(50):
            yield Tick()

    sim.add_sync_process(process)
    with sim.write_vcd("test.vcd", "test.gtkw", traces = [sync.clk, sync.rst] + simple.ports()):
        sim.run()

    
