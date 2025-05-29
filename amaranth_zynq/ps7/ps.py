from amaranth import Elaboratable, Signal, Module, Instance, Record
from .layouts import get_ps_layout, get_axi_layout

__all__ = ['ZynqPS']

def PsSignal(*argc, dir=None, **argv):
    s = Signal(*argc, **argv)
    s.dir = dir
    return s

class PsPorts:
    def __init__(self, ports):
        for k, v in ports.items():
            setattr(self, k.lower(), v)

class ZynqPS(Elaboratable):
    MAXI = ['maxigp0', 'maxigp1']
    SAXI = ['saxigp0', 'saxigp1']
    IRQ  = 'IRQF2P'                 # IRQ from PL
    CLK  = 'FCLKCLK'                # PL Clock

    DEFAULT_ONE = [
        'EMIOENET0TXRSOP', 'EMIOENET0TXREOP',
        'EMIOENET1TXRSOP', 'EMIOENET1TXREOP',
        'EMIOENET2TXRSOP', 'EMIOENET2TXREOP',
        'EMIOENET3TXRSOP', 'EMIOENET3TXREOP',
        'EMIOSDIO0WP', 'EMIOSDIO1WP',
        'EMIOSPI0SSIN', 'EMIOSPI1SSIN',
        'NFIQ0LPDRPU', 'NIRQ0LPDRPU',
        'NFIQ1LPDRPU', 'NIRQ1LPDRPU',
    ]

    def __init__(self):
        self._ports = self._get_ps_ports(get_ps_layout())
        self._clocks = [None for _ in range(4)]
        self._resets = [None for _ in range(4)]
        self._irqs = [None for _ in range(16)]
        self.ports = PsPorts(self._ports)

    def _get_instance_ports(self):
        ports = {}
        for pin, signal in self._ports.items():
            if signal.dir == 'input':
                prefix = 'i_'
            elif signal.dir == 'output':
                prefix = 'o_'
            else:
                prefix = 'o_'
            ports[prefix + pin] = signal
        return ports

    def _get_ps_ports(self, layout):
        return {
            pin: PsSignal(width, name=pin.lower(), reset=pin in self.DEFAULT_ONE, dir=direction)
            for pin, width, direction in layout
        }

    def get_clock_signal(self, n, freq):
        assert n < 4
        assert self._clocks[n] is None, ('Clock already taken')
        clk = Signal(name='pl_clk{}'.format(n))
        self._clocks[n] = (clk, freq)
        return clk

    def get_reset_signal(self, n):
        assert n < 4
        assert self._resets[n] is None, ('Clock already taken')
        rst = Signal(name='pl_reset{}'.format(n))
        self._resets[n] = rst
        return rst

    def get_irq_signal(self, n):
        assert n < 16
        assert self._irqs[n] is None, ('IRQ already taken')
        irq = Signal(name='irq{}'.format(n))
        self._irqs[n] = irq
        return irq

    def get_axi(self, axi):
        assert axi in self.MAXI + self.SAXI
        if axi in self.MAXI:
            layout = get_axi_layout('master')
        elif axi in self.SAXI:
            layout = get_axi_layout('slave')
        fields = {f: self._ports[axi.upper() + f] for f, w, d in layout}
        layout = [(f, w) for f, w, _ in layout]
        rec = Record(layout, fields=fields, name=axi)
        return rec

    def elaborate(self, platform):
        m = Module()
        for i, val in enumerate(self._clocks):
            if val is not None:
                clk, freq = val
                unbuf = Signal(name='pl_clk{}_unbuf'.format(i))
                platform.add_clock_constraint(unbuf, freq)

                m.d.comb += unbuf.eq(self._ports[self.CLK][i])
                buf = Instance(
                    'BUFG',
                     i_I=unbuf,
                     o_O=clk
                );
                m.submodules['clk{}_buffer'.format(i)] = buf

        for i, rst in enumerate(self._resets):
            if rst is not None:
                m.d.comb += rst.eq(~self._ports['EMIOGPIOO'][-1 - i])

        for i, irq in enumerate(self._irqs):
            if irq is not None:
                m.d.comb += self._ports[self.IRQ][i % 16].eq(irq)

        ps_i = Instance(
            'PS7',
            a_DONT_TOUCH="true",
            **self._get_instance_ports(),
        )

        m.submodules.ps_i = ps_i

        return m
