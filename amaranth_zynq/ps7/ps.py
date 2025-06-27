#

from amaranth import *
from amaranth.hdl import IOPort
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

from amaranth_wb2axip import AXI3, AXI4
from amaranth_zynq.interfaces import *

__all__ = ['PsZynq']

class PsZynq(wiring.Component):
    MAXIGP0: Out(AXI4(32, 32, 12))
    MAXIGP0ACLK: In(1)
    MAXIGP0ARESETN: Out(1)
    MAXIGP1: Out(AXI4(32, 32, 12))
    MAXIGP1ACLK: In(1)
    MAXIGP1ARESETN: Out(1)

    SAXIACP: In(AXI3(64, 32, 3))
    SAXIACPARESETN: Out(1)
    SAXIACPACLK: In(1)
    SAXIACPARUSER: In(5)
    SAXIACPAWUSER: In(5)
    SAXIACPARQOS: In(4)
    SAXIACPAWQOS: In(4)

    SAXIGP0: In(AXI3(32, 32, 6))
    SAXIGP0ACLK: In(1)
    SAXIGP0ARESETN: Out(1)
    SAXIGP0ARQOS: In(4)
    SAXIGP0AWQOS: In(4)
    SAXIGP1: In(AXI3(32, 32, 6))
    SAXIGP1ACLK: In(1)
    SAXIGP1ARESETN: Out(1)
    SAXIGP1ARQOS: In(4)
    SAXIGP1AWQOS: In(4)

    SAXIHP0: In(AXI3(64, 32, 6))
    SAXIHP0ACLK: In(1)
    SAXIHP0ARESETN: Out(1)
    SAXIHP0RACOUNT: Out(3)
    SAXIHP0RCOUNT: Out(8)
    SAXIHP0WACOUNT: Out(6)
    SAXIHP0WCOUNT: Out(8)
    SAXIHP0ARQOS: In(4)
    SAXIHP0AWQOS: In(4)
    SAXIHP0RDISSUECAP1EN: In(1)
    SAXIHP0WRISSUECAP1EN: In(1)
    SAXIHP1: In(AXI3(64, 32, 6))
    SAXIHP1ACLK: In(1)
    SAXIHP1ARESETN: Out(1)
    SAXIHP1RACOUNT: Out(3)
    SAXIHP1RCOUNT: Out(8)
    SAXIHP1WACOUNT: Out(6)
    SAXIHP1WCOUNT: Out(8)
    SAXIHP1ARQOS: In(4)
    SAXIHP1AWQOS: In(4)
    SAXIHP1RDISSUECAP1EN: In(1)
    SAXIHP1WRISSUECAP1EN: In(1)
    SAXIHP2: In(AXI3(64, 32, 6))
    SAXIHP2ACLK: In(1)
    SAXIHP2ARESETN: Out(1)
    SAXIHP2RACOUNT: Out(3)
    SAXIHP2RCOUNT: Out(8)
    SAXIHP2WACOUNT: Out(6)
    SAXIHP2WCOUNT: Out(8)
    SAXIHP2ARQOS: In(4)
    SAXIHP2AWQOS: In(4)
    SAXIHP2RDISSUECAP1EN: In(1)
    SAXIHP2WRISSUECAP1EN: In(1)
    SAXIHP3: In(AXI3(64, 32, 6))
    SAXIHP3ACLK: In(1)
    SAXIHP3ARESETN: Out(1)
    SAXIHP3RACOUNT: Out(3)
    SAXIHP3RCOUNT: Out(8)
    SAXIHP3WACOUNT: Out(6)
    SAXIHP3WCOUNT: Out(8)
    SAXIHP3ARQOS: In(4)
    SAXIHP3AWQOS: In(4)
    SAXIHP3RDISSUECAP1EN: In(1)
    SAXIHP3WRISSUECAP1EN: In(1)

    EMIOCAN0: Out(CAN())
    EMIOCAN1: Out(CAN())
    EMIOI2C0: Out(I2C())
    EMIOI2C1: Out(I2C())
    EMIOSPI0: Out(SPI())
    EMIOSPI1: Out(SPI())
    EMIOUART0: Out(UART())
    EMIOUART1: Out(UART())
    EMIOGPIO: Out(GPIO(64))
    EMIOTTC0: Out(TTC())
    EMIOTTC1: Out(TTC())
    EMIOWDT: Out(WDT())
    EMIOPJTAG: Out(PJTag_PS7())
    EMIOUSB0: Out(USB_PS7())
    EMIOUSB1: Out(USB_PS7())

    DMA0: Out(DMA_PS7())
    DMA1: Out(DMA_PS7())
    DMA2: Out(DMA_PS7())
    DMA3: Out(DMA_PS7())

    EMIOENET0: Out(ENET_PS7())
    EMIOENET1: Out(ENET_PS7())
    EMIOSDIO0: Out(SDIO_PS7())
    EMIOSDIO1: Out(SDIO_PS7())

    # Trace
    EMIOTRACECTL: Out(1)
    EMIOTRACEDATA: Out(32)
    EMIOTRACECLK: In(1)

    # SRAM
    EMIOSRAMINTIN: In(1)

    # PL Clock and Reset
    FCLKCLK: Out(4)
    FCLKCLKTRIGN: In(4)
    FCLKRESETN: Out(4)

    # PL Idle
    FPGAIDLEN: In(1)

    # Event
    EVENTEVENTI: In(1)
    EVENTEVENTO: Out(1)
    EVENTSTANDBYWFE: Out(2)
    EVENTSTANDBYWFI: Out(2)

    # DDR ARB
    DDRARB: In(4)

    # PL Trace
    FTMDTRACEINDATA: In(32)
    FTMDTRACEINVALID: In(1)
    FTMDTRACEINCLOCK: In(1)
    FTMDTRACEINATID: In(4)

    # Cross Trigger
    FTMTF2PTRIG: In(4)
    FTMTF2PTRIGACK: Out(4)
    FTMTP2FDEBUG: Out(32)
    FTMTP2FTRIG: Out(4)
    FTMTP2FTRIGACK: In(4)
    FTMTF2PDEBUG: In(32)

    # Interrupts
    IRQP2F: Out(29)
    IRQF2P: In(20)

    _BIDIRECTIONAL_PORTS = [
        ("DDRA", 15),
        ("DDRBA", 3),
        ("DDRCASB", 1),
        ("DDRCKE", 1),
        ("DDRCKN", 1),
        ("DDRCKP", 1),
        ("DDRCSB", 1),
        ("DDRDM", 4),
        ("DDRDQ", 32),
        ("DDRDQSN", 4),
        ("DDRDQSP", 4),
        ("DDRDRSTB", 1),
        ("DDRODT", 1),
        ("DDRRASB", 1),
        ("DDRVRN", 1),
        ("DDRVRP", 1),
        ("DDRWEB", 1),
        ("MIO", 54),
        ("PSCLK", 1),
        ("PSPORB", 1),
        ("PSSRSTB", 1),
    ]

    def __init__(self):
        super().__init__()
        self._clocks = [None for _ in range(4)]
        self._resets = [None for _ in range(4)]
        self._irqs = [None for _ in range(16)]

    def get_clock_signal(self, n, freq):
        assert n < 4
        assert self._clocks[n] is None, ('Clock already taken')
        clk = Signal(name='pl_clk{}'.format(n))
        self._clocks[n] = (clk, freq)
        return clk

    def get_irq_signal(self, n):
        assert n < 16
        assert self._irqs[n] is None, ('IRQ already taken')
        irq = Signal(name='irq{}'.format(n))
        self._irqs[n] = irq
        return irq

    def get_reset_signal(self, n):
        assert n < 4
        assert self._resets[n] is None, ('Reset already taken')
        rst = Signal(name='pl_reset{}'.format(n))
        self._resets[n] = rst
        return rst

    def _get_instance_ports(self, m):
        ports = {}
        for name, sig in self.signature.members.items():
            if sig.is_port:
                ports[('i_' if sig.flow == In else 'o_') + name] = getattr(self, name)
            else:
                ports.update(getattr(self, name).get_ports_for_instance(name))
        def expand_oport(port_name, sz):
            port = ports[port_name]
            if sz == 0:
                del ports[port_name]
            else:
                ports[port_name] = port[:sz]
            m.d.comb += port[sz:].eq(0)
        def shrink_oport(port_name, sz):
            port = ports[port_name]
            assert len(port) < sz
            dummy = Signal(sz - len(port))
            ports[port_name] = Cat(port, dummy)
        def fix_cache(name):
            m_port = ports[name]
            i_port = Signal(4, name=name)
            ports[name] = i_port
            m.d.comb += m_port.eq(Cat(i_port[0], Const(1), i_port[2:]))
        for maxigp in ("MAXIGP0", "MAXIGP1"):
            expand_oport(f"o_{maxigp}ARSIZE", 2)
            expand_oport(f"o_{maxigp}AWSIZE", 2)
            expand_oport(f"o_{maxigp}ARLEN", 4)
            expand_oport(f"o_{maxigp}AWLEN", 4)

            # Currently not defined by wb2axip
            # expand_oport(f"o_{maxigp}ARREGION", 0)
            # expand_oport(f"o_{maxigp}AWREGION", 0)

            shrink_oport(f"o_{maxigp}ARLOCK", 2)
            shrink_oport(f"o_{maxigp}AWLOCK", 2)

            fix_cache(f"o_{maxigp}ARCACHE")
            fix_cache(f"o_{maxigp}AWCACHE")
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

                m.d.comb += unbuf.eq(self.FCLKCLK[i])
                buf = Instance(
                    'BUFG',
                     i_I=unbuf,
                     o_O=clk
                );
                m.submodules['clk{}_buffer'.format(i)] = buf

        for i, rst in enumerate(self._resets):
            if rst is not None:
                m.d.comb += rst.eq(~self.FCLKRESETN[i])

        for i, irq in enumerate(self._irqs):
            if irq is not None:
                m.d.comb += self.IRQF2P[i % 16].eq(irq)

        ps_i = Instance(
            'PS7',
            a_DONT_TOUCH="true",
            **self._get_instance_ports(m),
        )

        m.submodules.ps_i = ps_i
        return m
