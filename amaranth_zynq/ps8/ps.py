#

from amaranth import Signal, Module, Instance
from amaranth.hdl import IOPort
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

from amaranth_wb2axip import AXI4, ACE
from amaranth_zynq.interfaces import *

class PsZynqMP(wiring.Component):
    MAXIGP0: Out(AXI4(128, 40, 16, 16))
    MAXIGP0ACLK: In(1)
    MAXIGP1: Out(AXI4(128, 40, 16, 16))
    MAXIGP1ACLK: In(1)
    MAXIGP2: Out(AXI4(128, 40, 16, 16))
    MAXIGP2ACLK: In(1)

    SAXIACP: In(AXI4(128, 40, 5, 2))
    SAXIACPACLK: In(1)

    SAXIGP0: In(AXI4(128, 49, 6, 1))
    SAXIGP0WCLK: In(1)
    SAXIGP0RCLK: In(1)
    SAXIGP0WACOUNT: Out(4)
    SAXIGP0WCOUNT: Out(8)
    SAXIGP0RACOUNT: Out(4)
    SAXIGP0RCOUNT: Out(8)
    SAXIGP1: In(AXI4(128, 49, 6, 1))
    SAXIGP1WCLK: In(1)
    SAXIGP1RCLK: In(1)
    SAXIGP1WACOUNT: Out(4)
    SAXIGP1WCOUNT: Out(8)
    SAXIGP1RACOUNT: Out(4)
    SAXIGP1RCOUNT: Out(8)
    SAXIGP2: In(AXI4(128, 49, 6, 1))
    SAXIGP2WCLK: In(1)
    SAXIGP2RCLK: In(1)
    SAXIGP2WACOUNT: Out(4)
    SAXIGP2WCOUNT: Out(8)
    SAXIGP2RACOUNT: Out(4)
    SAXIGP2RCOUNT: Out(8)
    SAXIGP3: In(AXI4(128, 49, 6, 1))
    SAXIGP3WCLK: In(1)
    SAXIGP3RCLK: In(1)
    SAXIGP3WACOUNT: Out(4)
    SAXIGP3WCOUNT: Out(8)
    SAXIGP3RACOUNT: Out(4)
    SAXIGP3RCOUNT: Out(8)
    SAXIGP4: In(AXI4(128, 49, 6, 1))
    SAXIGP4WCLK: In(1)
    SAXIGP4RCLK: In(1)
    SAXIGP4RACOUNT: Out(4)
    SAXIGP4RCOUNT: Out(8)
    SAXIGP4WACOUNT: Out(4)
    SAXIGP4WCOUNT: Out(8)
    SAXIGP5: In(AXI4(128, 49, 6, 1))
    SAXIGP5WCLK: In(1)
    SAXIGP5RCLK: In(1)
    SAXIGP5WACOUNT: Out(4)
    SAXIGP5WCOUNT: Out(8)
    SAXIGP5RACOUNT: Out(4)
    SAXIGP5RCOUNT: Out(8)
    SAXIGP6: In(AXI4(128, 49, 6, 1))
    SAXIGP6WCLK: In(1)
    SAXIGP6RCLK: In(1)
    SAXIGP6WACOUNT: Out(4)
    SAXIGP6WCOUNT: Out(8)
    SAXIGP6RACOUNT: Out(4)
    SAXIGP6RCOUNT: Out(8)

    SACEFPD: In(ACE(128, 44, 6, 1))
    SACEFPDBUSER: Out(1)
    SACEFPDRUSER: Out(1)
    SACEFPDARREGION: In(4)
    SACEFPDAWREGION: In(4)
    SACEFPDWUSER: In(1)

    EMIOCAN0: Out(CAN())
    EMIOCAN1: Out(CAN())
    EMIOI2C0: Out(I2C())
    EMIOI2C1: Out(I2C())
    EMIOSPI0: Out(SPI())
    EMIOSPI1: Out(SPI())
    EMIOUART0: Out(UART())
    EMIOUART1: Out(UART())
    EMIOSDIO0: Out(SDIO_PS8())
    EMIOSDIO1: Out(SDIO_PS8())
    EMIOGPIO: Out(GPIO(96))
    EMIOTTC0: Out(TTC())
    EMIOTTC1: Out(TTC())
    EMIOTTC2: Out(TTC())
    EMIOTTC3: Out(TTC())
    EMIOWDT0: Out(WDT())
    EMIOWDT1: Out(WDT())
    EMIOENET0: Out(ENET_PS8(gmii=True, mdio=True))
    EMIOENET1: Out(ENET_PS8(gmii=True, mdio=True))
    EMIOENET2: Out(ENET_PS8(gmii=True, mdio=True))
    EMIOENET3: Out(ENET_PS8(gmii=True, mdio=True))

    # Event IO
    PLPSEVENTI: In(1)
    PSPLEVENTO: Out(1)
    PSPLSTANDBYWFE: Out(4)
    PSPLSTANDBYWFI: Out(4)

    # FTM
    PLPSTRIGACK: In(4)
    PLPSTRIGGER: In(4)
    PSPLTRIGACK: Out(4)
    PSPLTRIGGER: Out(4)
    FTMGPO: Out(32)
    FTMGPI: In(32)

    # TSU
    FMIOGEMTSUCLKFROMPL: In(1)
    EMIOGEM0TSUINCCTRL: In(2)
    EMIOGEM1TSUINCCTRL: In(2)
    EMIOGEM2TSUINCCTRL: In(2)
    EMIOGEM3TSUINCCTRL: In(2)
    EMIOGEM0TSUTIMERCMPVAL: Out(1)
    EMIOGEM1TSUTIMERCMPVAL: Out(1)
    EMIOGEM2TSUTIMERCMPVAL: Out(1)
    EMIOGEM3TSUTIMERCMPVAL: Out(1)
    EMIOENET0GEMTSUTIMERCNT: Out(94)

    # PL_CLK
    PLCLK: Out(4)

    # PL_PS_IRQ
    PLPSIRQ0: In(8)
    PLPSIRQ1: In(8)

    # Trace0
    PSPLTRACECTL: Out(1)
    PSPLTRACEDATA: Out(32)

    ADMA2PLCACK: Out(8)
    ADMA2PLTVLD: Out(8)
    DPAUDIOREFCLK: Out(1)
    DPAUXDATAOEN: Out(1)
    DPAUXDATAOUT: Out(1)
    DPLIVEVIDEODEOUT: Out(1)
    DPMAXISMIXEDAUDIOTDATA: Out(32)
    DPMAXISMIXEDAUDIOTID: Out(1)
    DPMAXISMIXEDAUDIOTVALID: Out(1)
    DPSAXISAUDIOTREADY: Out(1)
    DPVIDEOOUTHSYNC: Out(1)
    DPVIDEOOUTPIXEL1: Out(36)
    DPVIDEOOUTVSYNC: Out(1)
    DPVIDEOREFCLK: Out(1)
    EMIOGEM0DELAYREQRX: Out(1)
    EMIOGEM0DELAYREQTX: Out(1)
    EMIOGEM0PDELAYREQRX: Out(1)
    EMIOGEM0PDELAYREQTX: Out(1)
    EMIOGEM0PDELAYRESPRX: Out(1)
    EMIOGEM0PDELAYRESPTX: Out(1)
    EMIOGEM0RXSOF: Out(1)
    EMIOGEM0SYNCFRAMERX: Out(1)
    EMIOGEM0SYNCFRAMETX: Out(1)
    EMIOGEM0TXRFIXEDLAT: Out(1)
    EMIOGEM0TXSOF: Out(1)
    EMIOGEM1DELAYREQRX: Out(1)
    EMIOGEM1DELAYREQTX: Out(1)
    EMIOGEM1PDELAYREQRX: Out(1)
    EMIOGEM1PDELAYREQTX: Out(1)
    EMIOGEM1PDELAYRESPRX: Out(1)
    EMIOGEM1PDELAYRESPTX: Out(1)
    EMIOGEM1RXSOF: Out(1)
    EMIOGEM1SYNCFRAMERX: Out(1)
    EMIOGEM1SYNCFRAMETX: Out(1)
    EMIOGEM1TXRFIXEDLAT: Out(1)
    EMIOGEM1TXSOF: Out(1)
    EMIOGEM2DELAYREQRX: Out(1)
    EMIOGEM2DELAYREQTX: Out(1)
    EMIOGEM2PDELAYREQRX: Out(1)
    EMIOGEM2PDELAYREQTX: Out(1)
    EMIOGEM2PDELAYRESPRX: Out(1)
    EMIOGEM2PDELAYRESPTX: Out(1)
    EMIOGEM2RXSOF: Out(1)
    EMIOGEM2SYNCFRAMERX: Out(1)
    EMIOGEM2SYNCFRAMETX: Out(1)
    EMIOGEM2TXRFIXEDLAT: Out(1)
    EMIOGEM2TXSOF: Out(1)
    EMIOGEM3DELAYREQRX: Out(1)
    EMIOGEM3DELAYREQTX: Out(1)
    EMIOGEM3PDELAYREQRX: Out(1)
    EMIOGEM3PDELAYREQTX: Out(1)
    EMIOGEM3PDELAYRESPRX: Out(1)
    EMIOGEM3PDELAYRESPTX: Out(1)
    EMIOGEM3RXSOF: Out(1)
    EMIOGEM3SYNCFRAMERX: Out(1)
    EMIOGEM3SYNCFRAMETX: Out(1)
    EMIOGEM3TXRFIXEDLAT: Out(1)
    EMIOGEM3TXSOF: Out(1)
    EMIOU2DSPORTVBUSCTRLUSB30: Out(1)
    EMIOU2DSPORTVBUSCTRLUSB31: Out(1)
    EMIOU3DSPORTVBUSCTRLUSB30: Out(1)
    EMIOU3DSPORTVBUSCTRLUSB31: Out(1)
    FMIOGEM0FIFORXCLKTOPLBUFG: Out(1)
    FMIOGEM0FIFOTXCLKTOPLBUFG: Out(1)
    FMIOGEM1FIFORXCLKTOPLBUFG: Out(1)
    FMIOGEM1FIFOTXCLKTOPLBUFG: Out(1)
    FMIOGEM2FIFORXCLKTOPLBUFG: Out(1)
    FMIOGEM2FIFOTXCLKTOPLBUFG: Out(1)
    FMIOGEM3FIFORXCLKTOPLBUFG: Out(1)
    FMIOGEM3FIFOTXCLKTOPLBUFG: Out(1)
    FMIOGEMTSUCLKTOPLBUFG: Out(1)
    GDMA2PLCACK: Out(8)
    GDMA2PLTVLD: Out(8)
    OSCRTCCLK: Out(1)
    PMUAIBAFIFMFPDREQ: Out(1)
    PMUAIBAFIFMLPDREQ: Out(1)
    PMUERRORTOPL: Out(47)
    PMUPLGPO: Out(32)
    PSPLIRQFPD: Out(64)
    PSPLIRQLPD: Out(100)
    PSS_ALTO_CORE_PAD_MGTTXN0OUT: Out(1)
    PSS_ALTO_CORE_PAD_MGTTXN1OUT: Out(1)
    PSS_ALTO_CORE_PAD_MGTTXN2OUT: Out(1)
    PSS_ALTO_CORE_PAD_MGTTXN3OUT: Out(1)
    PSS_ALTO_CORE_PAD_MGTTXP0OUT: Out(1)
    PSS_ALTO_CORE_PAD_MGTTXP1OUT: Out(1)
    PSS_ALTO_CORE_PAD_MGTTXP2OUT: Out(1)
    PSS_ALTO_CORE_PAD_MGTTXP3OUT: Out(1)
    PSS_ALTO_CORE_PAD_PADO: Out(1)
    RPUEVENTO0: Out(1)
    RPUEVENTO1: Out(1)

    ADMAFCICLK: In(8)
    AIBPMUAFIFMFPDACK: In(1)
    AIBPMUAFIFMLPDACK: In(1)
    DDRCEXTREFRESHRANK0REQ: In(1)
    DDRCEXTREFRESHRANK1REQ: In(1)
    DDRCREFRESHPLCLK: In(1)
    DPAUXDATAIN: In(1)
    DPEXTERNALCUSTOMEVENT1: In(1)
    DPEXTERNALCUSTOMEVENT2: In(1)
    DPEXTERNALVSYNCEVENT: In(1)
    DPHOTPLUGDETECT: In(1)
    DPLIVEGFXALPHAIN: In(8)
    DPLIVEGFXPIXEL1IN: In(36)
    DPLIVEVIDEOINDE: In(1)
    DPLIVEVIDEOINHSYNC: In(1)
    DPLIVEVIDEOINPIXEL1: In(36)
    DPLIVEVIDEOINVSYNC: In(1)
    DPMAXISMIXEDAUDIOTREADY: In(1)
    DPSAXISAUDIOCLK: In(1)
    DPSAXISAUDIOTDATA: In(32)
    DPSAXISAUDIOTID: In(1)
    DPSAXISAUDIOTVALID: In(1)
    DPVIDEOINCLK: In(1)
    EMIOENETTSUCLK: In(1)
    EMIOHUBPORTOVERCRNTUSB20: In(1)
    EMIOHUBPORTOVERCRNTUSB21: In(1)
    EMIOHUBPORTOVERCRNTUSB30: In(1)
    EMIOHUBPORTOVERCRNTUSB31: In(1)
    FMIOGEM0FIFORXCLKFROMPL: In(1)
    FMIOGEM0FIFOTXCLKFROMPL: In(1)
    FMIOGEM0SIGNALDETECT: In(1)
    FMIOGEM1FIFORXCLKFROMPL: In(1)
    FMIOGEM1FIFOTXCLKFROMPL: In(1)
    FMIOGEM1SIGNALDETECT: In(1)
    FMIOGEM2FIFORXCLKFROMPL: In(1)
    FMIOGEM2FIFOTXCLKFROMPL: In(1)
    FMIOGEM2SIGNALDETECT: In(1)
    FMIOGEM3FIFORXCLKFROMPL: In(1)
    FMIOGEM3FIFOTXCLKFROMPL: In(1)
    FMIOGEM3SIGNALDETECT: In(1)
    GDMAFCICLK: In(8)
    NFIQ0LPDRPU: In(1, init=1)
    NFIQ1LPDRPU: In(1, init=1)
    NIRQ0LPDRPU: In(1, init=1)
    NIRQ1LPDRPU: In(1, init=1)
    PL2ADMACVLD: In(8)
    PL2ADMATACK: In(8)
    PL2GDMACVLD: In(8)
    PL2GDMATACK: In(8)
    PLACECLK: In(1)
    PLACPINACT: In(1)
    PLFPGASTOP: In(4)
    PLLAUXREFCLKFPD: In(3)
    PLLAUXREFCLKLPD: In(2)
    PLPMUGPI: In(32)
    PLPSAPUGICFIQ: In(4)
    PLPSAPUGICIRQ: In(4)
    PLPSTRACECLK: In(1)
    PMUERRORFROMPL: In(4)
    PSS_ALTO_CORE_PAD_MGTRXN0IN: In(1)
    PSS_ALTO_CORE_PAD_MGTRXN1IN: In(1)
    PSS_ALTO_CORE_PAD_MGTRXN2IN: In(1)
    PSS_ALTO_CORE_PAD_MGTRXN3IN: In(1)
    PSS_ALTO_CORE_PAD_MGTRXP0IN: In(1)
    PSS_ALTO_CORE_PAD_MGTRXP1IN: In(1)
    PSS_ALTO_CORE_PAD_MGTRXP2IN: In(1)
    PSS_ALTO_CORE_PAD_MGTRXP3IN: In(1)
    PSS_ALTO_CORE_PAD_PADI: In(1)
    PSS_ALTO_CORE_PAD_REFN0IN: In(1)
    PSS_ALTO_CORE_PAD_REFN1IN: In(1)
    PSS_ALTO_CORE_PAD_REFN2IN: In(1)
    PSS_ALTO_CORE_PAD_REFN3IN: In(1)
    PSS_ALTO_CORE_PAD_REFP0IN: In(1)
    PSS_ALTO_CORE_PAD_REFP1IN: In(1)
    PSS_ALTO_CORE_PAD_REFP2IN: In(1)
    PSS_ALTO_CORE_PAD_REFP3IN: In(1)
    RPUEVENTI0: In(1)
    RPUEVENTI1: In(1)
    STMEVENT: In(60)

    _BIDIRECTIONAL_PORTS = [
        ("PSS_ALTO_CORE_PAD_BOOTMODE", 4),
        ("PSS_ALTO_CORE_PAD_CLK", 1),
        ("PSS_ALTO_CORE_PAD_DONEB", 1),
        ("PSS_ALTO_CORE_PAD_DRAMA", 18),
        ("PSS_ALTO_CORE_PAD_DRAMACTN", 1),
        ("PSS_ALTO_CORE_PAD_DRAMALERTN", 1),
        ("PSS_ALTO_CORE_PAD_DRAMBA", 2),
        ("PSS_ALTO_CORE_PAD_DRAMBG", 2),
        ("PSS_ALTO_CORE_PAD_DRAMCK", 2),
        ("PSS_ALTO_CORE_PAD_DRAMCKE", 2),
        ("PSS_ALTO_CORE_PAD_DRAMCKN", 2),
        ("PSS_ALTO_CORE_PAD_DRAMCSN", 2),
        ("PSS_ALTO_CORE_PAD_DRAMDM", 9),
        ("PSS_ALTO_CORE_PAD_DRAMDQ", 72),
        ("PSS_ALTO_CORE_PAD_DRAMDQS", 9),
        ("PSS_ALTO_CORE_PAD_DRAMDQSN", 9),
        ("PSS_ALTO_CORE_PAD_DRAMODT", 2),
        ("PSS_ALTO_CORE_PAD_DRAMPARITY", 1),
        ("PSS_ALTO_CORE_PAD_DRAMRAMRSTN", 1),
        ("PSS_ALTO_CORE_PAD_ERROROUT", 1),
        ("PSS_ALTO_CORE_PAD_ERRORSTATUS", 1),
        ("PSS_ALTO_CORE_PAD_INITB", 1),
        ("PSS_ALTO_CORE_PAD_JTAGTCK", 1),
        ("PSS_ALTO_CORE_PAD_JTAGTDI", 1),
        ("PSS_ALTO_CORE_PAD_JTAGTDO", 1),
        ("PSS_ALTO_CORE_PAD_JTAGTMS", 1),
        ("PSS_ALTO_CORE_PAD_MIO", 78),
        ("PSS_ALTO_CORE_PAD_PORB", 1),
        ("PSS_ALTO_CORE_PAD_PROGB", 1),
        ("PSS_ALTO_CORE_PAD_RCALIBINOUT", 1),
        ("PSS_ALTO_CORE_PAD_SRSTB", 1),
        ("PSS_ALTO_CORE_PAD_ZQ", 1),
    ]

    def __init__(self):
        super().__init__()
        self._clocks = [None for _ in range(4)]
        self._resets = [None for _ in range(4)]
        self._irqs = [None for _ in range(16)]

    def get_clock_signal(self, n, freq):
        assert n < 4
        assert self._clocks[n] is None, (
            'Clock already taken')
        clk = Signal(name='pl_clk{}'.format(n))
        self._clocks[n] = (clk, freq)
        return clk

    def get_irq_signal(self, n):
        assert n < 16
        assert self._irqs[n] is None, (
            'IRQ already taken')
        irq = Signal(name='irq{}'.format(n))
        self._irqs[n] = irq
        return irq

    def get_reset_signal(self, n):
        assert n < 4
        assert self._resets[n] is None, (
            'Reset already taken')
        rst = Signal(name='pl_reset{}'.format(n))
        self._resets[n] = rst
        return rst

    def _get_instance_ports(self):
        ports = {}
        for name, sig in self.signature.members.items():
            if sig.is_port:
                ports[('i_' if sig.flow == In else 'o_') + name] = getattr(self, name)
            else:
                ports.update(getattr(self, name).get_ports_for_instance(name))
        for name, sz in self._BIDIRECTIONAL_PORTS:
            ports['o_' + name] = Signal(sz, name=name)
            # ports['io_' + name] = Signal(sz, name=name)
        return ports

    def elaborate(self, platform):
        m = Module()
        for i, val in enumerate(self._clocks):
            if val is not None:
                clk, freq = val
                unbuf = Signal(name='pl_clk{}_unbuf'.format(i))
                platform.add_clock_constraint(unbuf, freq)

                m.d.comb += unbuf.eq(self.PLCLK[i])
                buf = Instance(
                    'BUFG_PS',
                     i_I=unbuf,
                     o_O=clk
                );
                m.submodules['clk{}_buffer'.format(i)] = buf

        for i, rst in enumerate(self._resets):
            if rst is not None:
                m.d.comb += rst.eq(~self.EMIOGPIO.O[-1 - i])

        IRQ = (self.PLPSIRQ0, self.PLPSIRQ1)
        for i, irq in enumerate(self._irqs):
            if irq is not None:
                m.d.comb += IRQ[i // 8][i % 8].eq(irq)

        ps_i = Instance(
            'PS8',
            a_DONT_TOUCH="true",
            **self._get_instance_ports(),
        )

        m.submodules.ps_i = ps_i
        return m
