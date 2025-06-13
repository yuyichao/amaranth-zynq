from amaranth import *
from amaranth.lib.cdc import ResetSynchronizer
from amaranth_zynq.platform import ZedboardPlatform
from amaranth_zynq.ps7 import PsZynq

class Zedboard(Elaboratable):
    def elaborate(self, platform):
        m = Module()
        m.domains += ClockDomain("sync")
        m.submodules.ps = ps = PsZynq()

        cnt = Signal(29)
        m.d.sync += cnt.eq(cnt + 1)
        m.d.comb += ps.get_irq_signal(0).eq(cnt[-1])

        clk = ps.get_clock_signal(0, 200e6)
        m.d.comb += ClockSignal('sync').eq(clk)

        rst = ps.get_reset_signal(0)
        m.submodules.reset_sync = ResetSynchronizer(rst, domain="sync")

        return m

if __name__ == '__main__':

    bif = r"""
            all:
            {
                {{name}}.bit
            }
           """

    ZedboardPlatform(bif).build(elaboratable=Zedboard())
