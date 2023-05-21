from amaranth import *
from amaranth.build import *
from amaranth.lib.fifo import SyncFIFO

import sys
sys.path.insert(0,"..")
from boards.alchitry_cu import AlchitryCuPlatform
from lib.serial import *


class uart_test(Elaboratable):
    def elaborate(self, platform):

        uart    = platform.request("uart")
        leds    = platform.request("led")
        divisor = int(platform.default_clk_frequency // 115200)

        m = Module()

        # Create the uart
        m.submodules.serial = serial = AsyncSerial(divisor=divisor, pins=uart)

        # create the FIFO
        m.submodules.fifo = fifo = SyncFIFO(width=8, depth=4)

        m.d.comb += [
            # connect rx data out to fifo data in
            fifo.w_data.eq(serial.rx.data),
            # write data to fifo when received
            fifo.w_en.eq(serial.rx.rdy),
            # allow read when fifo is ready
            serial.rx.ack.eq(fifo.w_rdy),

            # connect tx data to fifo read out
            serial.tx.data.eq(fifo.r_data),
            # transmit data when available in fifo
            serial.tx.ack.eq(fifo.r_rdy),
            # enable read from fifo, makes next byte available on next cycle
            fifo.r_en.eq(fifo.r_rdy & serial.tx.rdy),
            # Show any errors on leds: red for parity, green for overflow, blue for frame
            leds.eq(Cat(Repl(serial.rx.rdy, 5), serial.rx.err.frame, serial.rx.err.overflow, serial.rx.err.parity))
        ]

        return m
    


if __name__ == '__main__':
    platform = AlchitryCuPlatform()
    platform.build(uart_test(), do_program=True)
