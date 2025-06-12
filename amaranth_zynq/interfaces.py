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
    class Interface(_Base.Interface):
        pass

    def __init__(self):
        super().__init__(dict(
            PHYTX=Out(1),
            PHYRX=In(1),
        ))

class I2C(_Base):
    class Interface(_Base.Interface):
        pass

    def __init__(self):
        super().__init__(dict(
            SCLO=Out(1),
            SCLTN=Out(1),
            SDAO=Out(1),
            SDATN=Out(1),
            SCLI=In(1),
            SDAI=In(1),
        ))

class SPI(_Base):
    class Interface(_Base.Interface):
        pass

    def __init__(self):
        super().__init__(dict(
            MO=Out(1),
            MOTN=Out(1),
            SCLKO=Out(1),
            SCLKTN=Out(1),
            SO=Out(1),
            SSNTN=Out(1),
            SSON=Out(3),
            STN=Out(1),
            MI=In(1),
            SCLKI=In(1),
            SI=In(1),
            SSIN=In(1, init=1),
        ))

class UART(_Base):
    class Interface(_Base.Interface):
        pass

    def __init__(self):
        super().__init__(dict(
            DTRN=Out(1),
            RTSN=Out(1),
            TX=Out(1),
            CTSN=In(1),
            DCDN=In(1),
            DSRN=In(1),
            RIN=In(1),
            RX=In(1),
        ))

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
        return type(self) is type(other) and self.width == other.width

class TTC(_Base):
    class Interface(_Base.Interface):
        pass

    def __init__(self):
        super().__init__(dict(
            WAVEO=Out(3),
            CLKI=In(3),
        ))

class WDT(_Base):
    class Interface(_Base.Interface):
        pass

    def __init__(self):
        super().__init__(dict(
            RSTO=Out(1),
            CLKI=In(1),
        ))

class DMA_PS7(_Base):
    class Interface(_Base.Interface):
        pass

    def __init__(self):
        super().__init__(dict(
            DAREADY=In(1),
            DATYPE=Out(2),
            DAVALID=Out(1),
            DRLAST=In(1),
            DRREADY=Out(1),
            DRTYPE=In(2),
            DRVALID=In(1),
            RSTN=Out(1),
            ACLK=In(1),
        ))

class PJTag_PS7(_Base):
    class Interface(_Base.Interface):
        pass

    def __init__(self):
        super().__init__(dict(
            TDO=Out(1),
            TDTN=Out(1),
            TCK=In(1),
            TDI=In(1),
            TMS=In(1),
        ))

class USB_PS7(_Base):
    class Interface(_Base.Interface):
        pass

    def __init__(self):
        super().__init__(dict(
            PORTINDCTL=Out(2),
            VBUSPWRSELECT=Out(1),
            VBUSPWRFAULT=In(1),
        ))

class SDIO_PS7(_Base):
    class Interface(_Base.Interface):
        pass

    def __init__(self):
        super().__init__(dict(
            CLK=Out(1),
            CLKFB=In(1),

            CMDO=Out(1),
            CMDI=In(1),
            CMDTN=Out(1),

            DATAO=Out(4),
            DATAI=In(4),
            DATATN=Out(4),

            CDN=In(1),
            WP=In(1, init=1),
            LED=Out(1),
            BUSPOW=Out(1),
            BUSVOLT=Out(3),
        ))

class ENET_PS7(_Base):
    class Interface(_Base.Interface):
        pass

    def __init__(self):
        super().__init__(dict(
            MDIOMDC=Out(1),
            MDIOO=Out(1),
            MDIOTN=Out(1),
            MDIOI=In(1),

            GMIITXD=Out(8),
            GMIITXEN=Out(1),
            GMIITXER=Out(1),
            GMIICOL=In(1),
            GMIICRS=In(1),
            GMIIRXCLK=In(1),
            GMIIRXD=In(8),
            GMIIRXDV=In(1),
            GMIIRXER=In(1),
            GMIITXCLK=In(1),

            PTPDELAYREQRX=Out(1),
            PTPDELAYREQTX=Out(1),
            PTPPDELAYREQRX=Out(1),
            PTPPDELAYREQTX=Out(1),
            PTPPDELAYRESPRX=Out(1),
            PTPPDELAYRESPTX=Out(1),
            PTPSYNCFRAMERX=Out(1),
            PTPSYNCFRAMETX=Out(1),
            SOFRX=Out(1),
            SOFTX=Out(1),
            EXTINTIN=In(1),
        ))

class SDIO_PS8(_Base):
    class Interface(_Base.Interface):
        pass

    def __init__(self):
        super().__init__(dict(
            BUSPOWER=Out(1),
            BUSVOLT=Out(3),
            CLKOUT=Out(1),
            CMDENA=Out(1),
            CMDOUT=Out(1),
            DATAENA=Out(8),
            DATAOUT=Out(8),
            LEDCONTROL=Out(1),
            CDN=In(1),
            CMDIN=In(1),
            DATAIN=In(8),
            FBCLKIN=In(1),
            WP=In(1, init=1),
        ))

class ENET_PS8(_Base):
    class Interface(_Base.Interface):
        pass

    def __init__(self, gmii, mdio):
        self._gmii = gmii
        self._mdio = mdio
        port = dict(
            DMABUSWIDTH=Out(2),
            DMATXENDTOG=Out(1),
            RXWDATA=Out(8),
            RXWEOP=Out(1),
            RXWERR=Out(1),
            RXWFLUSH=Out(1),
            RXWSOP=Out(1),
            RXWSTATUS=Out(45),
            RXWWR=Out(1),
            TXRRD=Out(1),
            TXRSTATUS=Out(4),
            DMATXSTATUSTOG=In(1),
            EXTINTIN=In(1),
            RXWOVERFLOW=In(1),
            TXRCONTROL=In(1),
            TXRDATA=In(8),
            TXRDATARDY=In(1),
            TXREOP=In(1, init=1),
            TXRERR=In(1),
            TXRFLUSHED=In(1),
            TXRSOP=In(1, init=1),
            TXRUNDERFLOW=In(1),
            TXRVALID=In(1),
        )
        if gmii:
            port.update(dict(
                GMIITXD=Out(8),
                GMIITXEN=Out(1),
                GMIITXER=Out(1),
                SPEEDMODE=Out(3),
                GMIICOL=In(1),
                GMIICRS=In(1),
                GMIIRXCLK=In(1),
                GMIIRXD=In(8),
                GMIIRXDV=In(1),
                GMIIRXER=In(1),
                GMIITXCLK=In(1),
            ))

        if mdio:
            port.update(dict(
                MDIOMDC=Out(1),
                MDIOO=Out(1),
                MDIOTN=Out(1),
                MDIOI=In(1),
            ))

        super().__init__(port)

    @property
    def gmii(self):
        return self._gmii

    @property
    def mdio(self):
        return self._mdio

    def __repr__(self):
        return f'ENET_PS8({self.gmii}, self.{mdio})'

    def __eq__(self, other):
        return (type(self) is type(other) and self.gmii == other.gmii and
                self.mdio == other.mdio)
