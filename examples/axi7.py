from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.cdc import ResetSynchronizer
from amaranth_zynq.platform import ZedboardPlatform
from amaranth_zynq.ps7 import PsZynq
from amaranth_wb2axip import AXI32AXI, AXI2AXILite, AXILiteXBar, DemoAXI


class AXIExample(Elaboratable):
    def elaborate(self, platform):
        m = Module()
        m.domains += ClockDomain('sync')
        m.submodules.ps = ps = PsZynq()

        clk = ps.get_clock_signal(0, 200e6)
        m.d.comb += ClockSignal().eq(clk)
        reset = ps.get_reset_signal(0)
        reset_sync = ResetSynchronizer(reset, domain="sync")
        m.submodules.reset_sync = reset_sync

        axi_master = ps.MAXIGP1
        m.d.comb += ps.MAXIGP1ACLK.eq(clk)

        m.submodules.axi2axil = axi2axil = AXI2AXILite(data_width=32,
                                                       addr_width=32,
                                                       id_width=12)
        wiring.connect(m, axi_master, axi2axil.axi)

        xbar = AXILiteXBar(data_width=32, addr_width=32)
        m.submodules.xbar = xbar
        xbar.add_master(axi2axil.axilite)

        for i in range(5):
            demo = DemoAXI(32, 16, 'sync')
            m.submodules['demo' + str(i)] = demo
            xbar.add_slave(demo.axilite.cast(m, addr_width=32),
                           0x1000 * i, 0x1000)

        return m


core = AXIExample()
plat = ZedboardPlatform()
plat.build(core)
