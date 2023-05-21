from amaranth import *
from amaranth.build import *
from amaranth.lib.fifo import SyncFIFO
from amaranth import Memory

import numpy as np
import math

import argparse
import sys
sys.path.insert(0,"..")
from boards.alchitry_cu import AlchitryCuPlatform
from lib.i2s_pcm5102_axis import *

class sine(Elaboratable):
    def elaborate(self, platform):

        Fs = 97656.25      # Sampling frequency
        f = 100           # Signal frequency
        A = 32767          # Amplitude
        norm_f = f / Fs
        N = 1 / norm_f     
        n = np.arange(N)

        y = A * np.sin(2*np.pi*n*norm_f)

        table = np.round(y).astype('i2')
        
        phi = int(table.size / 4 )          # 90 deg phase shift



        m = Module()

        mem = Memory(width=16, depth=table.size, init=table)

        # create the i2s output interface
        m.submodules.i2s = i2s = I2SOut()
        m.submodules.mem_port_l = mem_port_l = mem.read_port()
        m.submodules.mem_port_r = mem_port_r = mem.read_port()

        idx = Const(3)

        address_l = Signal(range(0, table.size), reset=0)
        address_r = Signal(range(0, table.size), reset=phi)


        m.d.comb += [
            i2s.samples[0].eq(mem_port_l.data),
            i2s.samples[1].eq(mem_port_r.data),
            mem_port_l.addr.eq(address_l),
            mem_port_r.addr.eq(address_r),
        ]

        with m.If(address_l == table.size):
            m.d.sync += [
                address_l.eq(0),
            ]
        with m.Elif(address_r == table.size):
            m.d.sync += [
                address_r.eq(0),
            ]
        with m.Elif(i2s.tready):
            m.d.sync += [
                #address.eq(address + 1)
                # increment address by index and correct for the overflow (fmod)
                address_l.eq(Mux((address_l + idx) > table.size, (address_l + idx - table.size), (address_l + idx))),
                address_r.eq(Mux((address_r + idx) > table.size, (address_r + idx - table.size), (address_r + idx))),
                
                i2s.tvalid.eq(1),
            ]
        with m.Else():
            m.d.sync += [
                i2s.tvalid.eq(0),
            ]

        # connect ports
        if(args.build):
            i2s_pins = platform.request("i2s")
            m.d.comb += [
                i2s_pins.eq(i2s.i2s)
            ]
            


        return m
        
    
if __name__ == '__main__':
    # use argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--simulate", action="store_true")
    parser.add_argument("-b", "--build",    action="store_true")
    parser.add_argument("-p", "--program",  action="store_true")

    args = parser.parse_args()

    if(args.simulate):
        dut = sine()
        sim = Simulator(dut)
        sim.add_clock(1e-8)

        def process():
            for i in range(100000):
                yield Tick()

        sim.add_sync_process(process)
        with sim.write_vcd("sine.vcd","sine.gtkw"):
            sim.run()



    elif(args.build):
        platform = AlchitryCuPlatform()
        platform.build(sine(), do_program=args.program)

    else:
        print("Please choose arguments -s to simulate, -b to build and -p to program")


    