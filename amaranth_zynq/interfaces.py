#

from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

class _Base(wiring.Signature):
    class Interface(wiring.PureInterface):
        def get_ports_for_instance(self, prefix=''):
            return self.signature.get_port_for_instance(self, prefix)

        @property
        def all_ports(self):
            return [signal for path, _, signal in self.signature.flatten(self)]

    def __repr__(self):
        return f'{type(self).__name__}()'

    def __eq__(self, other):
        return type(self) is type(other)

    def create(self, *, path=None, src_loc_at=0):
        return self.Interface(self, path=path, src_loc_at=src_loc_at + 1)

    def get_port_for_instance(self, iface, prefix=''):
        return {('i_' if port.flow is In else 'o_') + prefix + name: getattr(iface, name)
                for name, port in self.members.items()}

class CAN(_Base):
    PHYTX: Out(1)
    PHYRX: In(1)

    class Interface(_Base.Interface):
        pass

class I2C(_Base):
    SCLO: Out(1)
    SCLTN: Out(1)
    SDAO: Out(1)
    SDATN: Out(1)
    SCLI: In(1)
    SDAI: In(1)

    class Interface(_Base.Interface):
        pass

class SPI(_Base):
    MO: Out(1)
    MOTN: Out(1)
    SCLKO: Out(1)
    SCLKTN: Out(1)
    SO: Out(1)
    SSNTN: Out(1)
    SSON: Out(3)
    STN: Out(1)
    MI: In(1)
    SCLKI: In(1)
    SI: In(1)
    SSIN: In(1, init=1)

    class Interface(_Base.Interface):
        pass

class UART(_Base):
    DTRN: Out(1)
    RTSN: Out(1)
    TX: Out(1)
    CTSN: In(1)
    DCDN: In(1)
    DSRN: In(1)
    RIN: In(1)
    RX: In(1)

    class Interface(_Base.Interface):
        pass

class SDIO(_Base):
    BUSPOWER: Out(1)
    BUSVOLT: Out(3)
    CLKOUT: Out(1)
    CMDENA: Out(1)
    CMDOUT: Out(1)
    DATAENA: Out(8)
    DATAOUT: Out(8)
    LEDCONTROL: Out(1)
    CDN: In(1)
    CMDIN: In(1)
    DATAIN: In(8)
    FBCLKIN: In(1)
    WP: In(1, init=1)

    class Interface(_Base.Interface):
        pass

class GPIO(_Base):
    class Interface(_Base.Interface):
        pass

    def __init__(self, width):
        self._width = width
        super().__init__(dict(O=Out(width), TN=Out(width), I=In(width)))

    @property
    def width(self):
        return self._width

    def __repr__(self):
        return f'GPIO({self._width})'

    def __eq__(self, other):
        return type(self) is type(other) && self.width == other.width

class TTC(_Base):
    WAVEO: Out(3)
    CLKI: In(3)

    class Interface(_Base.Interface):
        pass

class WDT(_Base):
    RSTO: Out(1)
    CLKI: In(1)

    class Interface(_Base.Interface):
        pass
