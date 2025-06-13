from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.cdc import ResetSynchronizer
from amaranth_zynq.ps8 import PsZynqMP
from amaranth_zynq.platform import ZynqPlatform
from amaranth_wb2axip import AXI2AXILite, AXILiteXBar, DemoAXI


class Zu3egPlatform(ZynqPlatform):
    device     = 'xczu3eg'
    package    = 'sfva625'
    speed      = '1-e'
    resources  = []
    connectors = []


class AXIExample(Elaboratable):
    def elaborate(self, platform):
        m = Module()
        m.domains += ClockDomain('sync')
        m.submodules.ps = ps = PsZynqMP()

        clk = ps.get_clock_signal(0, 200e6)
        m.d.comb += ClockSignal().eq(clk)
        reset = ps.get_reset_signal(0)
        reset_sync = ResetSynchronizer(reset, domain="sync")
        m.submodules.reset_sync = reset_sync

        axi_master = ps.MAXIGP2.cast(m, user_width=0)
        m.d.comb += ps.MAXIGP2ACLK.eq(clk)

        axi2axil = AXI2AXILite(data_width=128, addr_width=40, id_width=16, domain='sync')
        m.submodules.axi2axil = axi2axil
        wiring.connect(m, axi_master, axi2axil.axi)

        xbar = AXILiteXBar(data_width=128, addr_width=40, domain='sync')
        m.submodules.xbar = xbar
        xbar.add_master(axi2axil.axilite)

        for i in range(5):
            demo = DemoAXI(128, 16, 'sync')
            m.submodules['demo' + str(i)] = demo
            xbar.add_slave(demo.axilite.cast(m, addr_width=40), 0x1000 * i, 0x1000)

        return m


core = AXIExample()
plat = Zu3egPlatform(bif=r"""
            all:
            {
                [destination_device = pl] {{name}}.bit
            }
        """)
plat.build(core)
