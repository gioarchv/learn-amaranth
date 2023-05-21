from amaranth import *
from amaranth.sim import *


class I2SOut(Elaboratable):

    """
    Inter-IC Sound (I2S) output.  Drives a Cirrus PCM5102 converter.

    This module is hardcoded to two channels, 16 bit samplesPCM internal PLL.
    BCK is 32 - clk_freq is 100 Mhz and divided by 100/32=3.125 Mhz
    with BCK of 32 it gives 3125/32=97.65625 kHz sampling rate.
    
    Samples are flow controlled by two signals, `stb` and `ack`.  The
    source should assert `stb` when a stereo sample is available, and
    this module asserts `ack` when the sample has been consumed.

    sample[0] is left channel, and sample[1] is right channel.
    """

    def __init__(self):
        self.i2s = Record([
            ('lrck', 1),
            ('bck', 1),
            ('din', 1),
        ])
        self.samples = Array((Signal(signed(16)), Signal(signed(16))))
        self.stb = Signal()
        self.ack = Signal()
        self.ports = [self.i2s.lrck, self.i2s.bck, self.i2s.din]
        self.ports += [self.samples[0], self.samples[1], self.stb, self.ack]

    def elaborate(self, platform):
        bitstream = Signal(32)
        cnt = Signal(10)
        bck = Signal()
        din = Signal()
        lrck = Signal()
        tmp = Signal(4)
        m = Module()


        with m.If((cnt == 0x020) & (self.stb == True)):
            m.d.sync += [
                # I2S bitstream is MSB first, so reverse bits here.
                bitstream.eq(Cat(self.samples[0][::-1], self.samples[1][::-1])),
                self.ack.eq(True),
            ]
        with m.Elif(cnt == 0x020):
            m.d.sync += [
                bitstream.eq(0),
                self.ack.eq(False),
            ]
        with m.Else():
            m.d.sync += [
                self.ack.eq(False),
            ]

        m.d.sync += [
            cnt.eq(cnt + 1),
            bck.eq(cnt[4]),
            tmp.eq(cnt[5:5+4] - 1),
            #din.eq(bitstream.bit_select(cnt[5:5+5] - 1, 1)),
            din.eq(bitstream.bit_select((Mux(cnt[5:5+5] == 0, 0x1F, (cnt[5:5+5] - 1))), 1)),    # correct for cnt[5:5+5] == 0
            lrck.eq(cnt[5 + 4]),
        ]
        
        m.d.comb += [
            self.i2s.bck.eq(bck),
            self.i2s.din.eq(din),
            self.i2s.lrck.eq(lrck),
        ]
        return m


if __name__ == '__main__':
    dut = I2SOut()
    
    sim = Simulator(dut)
    sim.add_clock(1e-8)

    def process():
        left = 0
        right = 0
        for i in range(24):
            yield dut.samples[0].eq(left)
            yield dut.samples[1].eq(right)
            yield dut.stb.eq(1)
            left = left + 1
            right = right + 1
            while (yield dut.ack) == 0:
                yield
            yield dut.stb.eq(0)
            yield

    sim.add_sync_process(process)
    with sim.write_vcd("I2SOut_pcm5102.vcd", "I2SOut_pcm5102.gtkw"):
        sim.run()
