#

from amaranth.build import *
from amaranth.vendor import XilinxPlatform

from amaranth_boards.resources import *

class ZynqPlatform(XilinxPlatform):
    def __init__(self, bif=None, **kwargs):
        self._bif = bif
        super().__init__(**kwargs)

    @property
    def required_tools(self):
        tools = super().required_tools
        if self._bif is not None:
            tools = [ *tools, "bootgen" ]
        return tools

    @property
    def file_templates(self):
        files = super().file_templates
        if self._bif is not None:
            files = { **files, "{{name}}.bif": self._bif }
        return files

    @property
    def command_templates(self):
        cmds = super().command_templates
        if self._bif is not None:
            if self.device.startswith("xc7z"):
                bootgencmd = r"""
                    {{invoke_tool("bootgen")}}
                        -image {{name}}.bif
                        -arch zynq
                        -w on
                        -o {{name}}_bootgen.bin
                """
            elif self.device.startswith("xczu"):
                bootgencmd = r"""
                    {{invoke_tool("bootgen")}}
                        -image {{name}}.bif
                        -arch zynqmp
                        -w on
                        -o {{name}}_bootgen.bin
                """
            else:
                raise ValueError(f"Invalid Zynq device {self.device}")
            cmds = [ *cmds, bootgencmd ]
        return cmds

class ZedboardPlatform(ZynqPlatform):
    device = "xc7z020"
    package = "clg484"
    speed = "1"
    default_clk = "clk100"    # Use GCLK as PL clock source

    def __init__(self, *args, VADJ="1V8", **kwargs):
        super().__init__(*args, **kwargs)

        if not VADJ in ("1V8", "2V5", "3V3"):
            raise RuntimeError("VADJ must be \"1V8\", \"2V5\", or \"3V3\"")

        self._VADJ = VADJ

    def bank34_35_iostandard(self):
        if self._VADJ == "1V8":
            return "LVCMOS18"
        elif self._VADJ == "2V5":
            return "LVCMOS25"
        elif self._VADJ == "3V3":
            return "LVCMOS33"

    """
    Add Zedboard PL resources via following documentations:
        1. https://github.com/Avnet/hdl/blob/master/Boards/ZEDBOARD/zedboard_master_XDC_RevC_D_v2.xdc
        2. https://files.digilent.com/resources/programmable-logic/zedboard/ZedBoard_HW_UG_v2_2.pdf
    """
    resources = [
        # Audio Codec - Bank 13
        Resource("audio_i2c", 0, # ADAU1761, I2C
            Subsignal("scl", Pins("AB4", dir="io")),    # AC-SCL, I2C Clock
            Subsignal("sda", Pins("AB5", dir="io")),    # AC-SDA, I2C Data
            Subsignal("adr", Pins("AB1 Y5", dir="o")),  # AC-ADR, I2C Address Bits
            Attrs(IOSTANDARD="LVCMOS33"),
        ),
        Resource("audio_i2s", 0, # ADAU1761, I2S
            Subsignal("clk",    Pins("AA6", dir="o")),  # AC-GPIO2, Bit Clock
            Subsignal("sd_adc", Pins("AA7", dir="o")),  # AC-GPIO1, Serial-Data ADC Output
            Subsignal("sd_dac", Pins("Y8",  dir="i")),  # AC-GPIO0, Serial-Data DAC Inpupt
            Subsignal("ws",     Pins("Y6",  dir="o")),  # AC-GPIO3, Left-Right Clock
            Attrs(IOSTANDARD="LVCMOS33"),
        ),
        Resource("audio_clk", 0, # ADAU1761, MCLK
            Subsignal("mclk", Pins("AB2", dir="o")),    # AC-MCLK, Master Clock
            Attrs(IOSTANDARD="LVCMOS33"),
        ),

        # Clock Source - Bank 13, 100Mhz
        Resource("clk100", 0, Pins("Y9", dir="i"), Clock(100e6),
                 Attrs(IOSTANDARD="LVCMOS33")), # GCLK

        # OLED Display - Bank 13
        SPIResource(0, # OLED, SSD1306, 128 x 32
            cs_n="dummy-cs0",
            clk="AB12",         # OLED-SCLK
            copi="AA12",        # OLED-DIN
            cipo="dummy-cpio0",
            reset="U9",         # OLED-RES
            attrs=Attrs(IOSTANDARD="LVCMOS33"),
        ),
        Resource("oled", 0, # OLED, UG-2832HSWEG04
            Subsignal("dc",      Pins ("U10", dir="o")),    # OLED-DC
            Subsignal("vdd_en",  PinsN("U12", dir="o")),    # OLED-VDD
            Subsignal("vbat_en", PinsN("U11", dir="o")),    # OLED-VBAT
            Attrs(IOSTANDARD="LVCMOS33"),
        ),

        # HDMI Output - Bank 33
        Resource("hdmi", 0, # ADV7511
            Subsignal("scl", Pins("AA18", dir="o")),     # HD-SCL, I2C Clock
            Subsignal("sda", Pins("Y16",  dir="io")),    # HD-SDA, I2C Data
            Subsignal("clk", Pins("W18",  dir="o")),     # HD-CLK, Video Clock
            Subsignal("vs",  Pins("W17",  dir="o")),     # HD-VSYNC, Vertical Sync
            Subsignal("hs",  Pins("V17",  dir="o")),     # HD-HSYNC, Horizontal Sync
            Subsignal("de",  Pins("U16",  dir="o")),     # HD-DE, Data Enable
            Subsignal("int", Pins("W16",  dir="i")),     # HD-INT, Interupt signal
            Subsignal("spdif", Pins("U15", dir="o")),    # HD-SPDIF, Sony/Philips audio in
            Subsignal("spdifo", Pins("Y18", dir="i")), # HD-SPDIFO, Sony/Philips audio out
            Subsignal("yuv", Pins("Y13 AA12 AA14 Y14 AB15 AB16 AA16 AB17 AA17 Y15 W13 W15 V15 U17 V14 V13", dir="o")),  # HD-D[15:0], Video Data in YCbCr 4:2:2 format
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        # User LEDs - Bank 33
        *LEDResources(pins={
            0: "T22",   # LD0
            1: "T21",   # LD1
            2: "U22",   # LD2
            3: "U21",   # LD3
            4: "V22",   # LD4
            5: "W22",   # LD5
            6: "U19",   # LD6
            7: "U14",   # LD7
        }, attrs=Attrs(IOSTANDARD="LVCMOS33")),

        # VGA Output - Bank 33
        VGAResource(
            0,
            r="V20  U20  V19  V18 ",
            g="AB22 AA22 AB21 AA21",
            b="Y21  Y20  AB20 AB19",
            hs="AA19", vs="Y19",
            attrs=Attrs(IOSTANDARD="LVCMOS33"),
        ),

        # User Push Bottons - Bank 34
        Resource("BTNC", 0, Pins("P16", dir="i"), Attrs(IOSTANDARD=bank34_35_iostandard)),
        Resource("BTND", 0, Pins("R16", dir="i"), Attrs(IOSTANDARD=bank34_35_iostandard)),
        Resource("BTNL", 0, Pins("N15", dir="i"), Attrs(IOSTANDARD=bank34_35_iostandard)),
        Resource("BTNR", 0, Pins("R18", dir="i"), Attrs(IOSTANDARD=bank34_35_iostandard)),
        Resource("BTNU", 0, Pins("T18", dir="i"), Attrs(IOSTANDARD=bank34_35_iostandard)),

        # USB OTG VBus OC - Bank 34
        Resource("OTG_VBUSOC", 0, Pins("L16", dir="i"),
                 Attrs(IOSTANDARD=bank34_35_iostandard)),

        # Miscellaneous - Bank 34
        Resource("PUDC_B", 0, Pins("K16", dir="i"),
                 Attrs(IOSTANDARD=bank34_35_iostandard)),

        # USB OTG Reset - Bank 35
        Resource("OTG_RESETN", 0, Pins("G17", dir="i"),
                 Attrs(IOSTANDARD=bank34_35_iostandard)),

        # User DIP Switches - Bank 35
        *SwitchResources(pins={
            0: "F22",   # SW0
            1: "G22",   # SW1
            2: "H22",   # SW2
            3: "F21",   # SW3
            4: "H19",   # SW4
            5: "H18",   # SW5
            6: "H17",   # SW6
            7: "M15",   # SW7
        }, attrs=Attrs(IOSTANDARD=bank34_35_iostandard)),
    ]

    connectors = [
                             #J1  J2   J3  J4      J7   J8   J9  J10
        Connector("pmod", 0, "Y11 AA11 Y10 AA9 - - AB11 AB10 AB9 AA8 - -"), # JA
        Connector("pmod", 1, "W12 W11  V10 W8  - - V12  W10  V9  V8  - -"), # JB
        Connector("pmod", 2, "AB6 ABA7 AA4 Y4  - - T6   R6   U4  T4  - -"), # JC
        Connector("pmod", 3, "W7  V7   V4  V5  - - W5   W6   U5  U6  - -"), # JD

        Connector("fmc", 0, {
            # Bank 13
            "SCL": "R7",
            "SDA": "U7",

            # Bank 33
            "PRSNT": "AB14",

            # Bank 34
            "CLK0_N": "L19",
            "CLK0_P": "L18",
            "LA00_CC_N": "M20",
            "LA00_CC_P": "M19",
            "LA01_CC_N": "N20",
            "LA00_CC_P": "N19",
            "LA02_N": "P18",
            "LA02_P": "P17",
            "LA03_N": "P22",
            "LA03_P": "N22",
            "LA04_N": "M22",
            "LA04_P": "M21",
            "LA05_N": "K18",
            "LA05_P": "J18",
            "LA06_N": "L22",
            "LA06_P": "L21",
            "LA07_N": "T17",
            "LA07_P": "T16",
            "LA08_N": "J22",
            "LA08_P": "J21",
            "LA09_N": "R21",
            "LA09_P": "R20",
            "LA10_N": "T19",
            "LA10_P": "R19",
            "LA11_N": "N18",
            "LA11_P": "N17",
            "LA12_N": "P21",
            "LA12_P": "P20",
            "LA13_N": "M17",
            "LA13_P": "L17",
            "LA14_N": "K20",
            "LA14_P": "K19",
            "LA15_N": "J17",
            "LA15_P": "J16",
            "LA16_N": "K21",
            "LA16_P": "J20",

            # Bank 35
            "CLK1_N": "C19",
            "CLK1_P": "D18",
            "LA17_CC_N": "B20",
            "LA17_CC_P": "B19",
            "LA18_CC_N": "C20",
            "LA18_CC_P": "D20",
            "LA19_N": "G16",
            "LA19_P": "G15",
            "LA20_N": "G21",
            "LA20_P": "G20",
            "LA21_N": "E20",
            "LA21_P": "E19",
            "LA22_N": "F19",
            "LA22_P": "G19",
            "LA23_N": "D15",
            "LA23_P": "E15",
            "LA24_N": "A19",
            "LA24_P": "A18",
            "LA25_N": "C22",
            "LA25_P": "D22",
            "LA26_N": "E18",
            "LA26_P": "F18",
            "LA27_N": "D21",
            "LA27_P": "E21",
            "LA28_N": "A17",
            "LA28_P": "A16",
            "LA29_N": "C18",
            "LA29_P": "C17",
            "LA30_N": "B15",
            "LA30_P": "C15",
            "LA31_N": "B17",
            "LA31_P": "B16",
            "LA32_N": "A22",
            "LA32_P": "A21",
            "LA33_N": "B22",
            "LA33_P": "B21",
        }),

        Connector("xadc", 0, {
            # XADC AD Channels - Bank 35
            "vaux0_n": "E16",
            "vaux0_p": "F16",
            "vaux8_n": "D17",
            "vaux8_p": "D16",

            # XADC GIO - Bank 34
            "gio0": "H15",
            "gio1": "R15",
            "gio2": "K15",
            "gio3": "J15",

            # XADC Inner Signals
            #"v_n": "M12",
            #"v_p": "L11",
            #"dx_n": "N12",  # Termal Diode diff pair N
            #"dx_p": "N11",  # Termal Diode diff pair P
        }),
    ]
