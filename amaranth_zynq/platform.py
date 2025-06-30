#

from amaranth.build import *
from amaranth.vendor import XilinxPlatform

from amaranth_boards.resources import *

class XilinxSoCPlatform(XilinxPlatform):
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

class ZedboardPlatform(XilinxSoCPlatform):
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


class ZC702Platform(XilinxSoCPlatform):
    device = "xc7z020"
    package = "clg484"
    speed = "1"
    default_clk = "clk156"

    def __init__(self, *args, VADJ="2V5", **kwargs):
        super().__init__(*args, **kwargs)

        if not VADJ in ("1V8", "2V5", "3V3"):
            raise RuntimeError("VADJ must be \"1V8\", \"2V5\", or \"3V3\"")

        self._VADJ = VADJ

    def bank_iostandard(self):
        if self._VADJ == "1V8":
            return "LVCMOS18"
        elif self._VADJ == "2V5":
            return "LVCMOS25"
        elif self._VADJ == "3V3":
            return "LVCMOS33"

    def bank_iostandard_ds(self):
        if self._VADJ == "1V8":
            return "LVDS18"
        elif self._VADJ == "2V5":
            return "LVDS25"
        elif self._VADJ == "3V3":
            return "LVDS33"

    """
    Add ZC702 PL resources via following documentations:
        https://docs.amd.com/v/u/en-US/ug850-zc702-eval-bd
    """
    resources = [
        Resource("sysclk", 0, DiffPairs("C19", "D18", dir="i"),
                 Clock(200e6), Attrs(IOSTANDARD=bank_iostandard_ds)),
        Resource("clk156", 0, DiffPairs("Y8", "Y9", dir="i"),
                 Clock(156e6), Attrs(IOSTANDARD=bank_iostandard_ds)),

        # HDMI Output
        Resource("hdmi", 0, # ADV7511
            Subsignal("de",  Pins("T18",  dir="o")),     # HD-DE, Data Enable
            Subsignal("spdif", Pins("R15", dir="o")),    # HD-SPDIF, Sony/Philips audio in
            Subsignal("clk", Pins("L16",  dir="o")),     # HD-CLK, Video Clock
            Subsignal("vs",  Pins("H15",  dir="o")),     # HD-VSYNC, Vertical Sync
            Subsignal("hs",  Pins("R18",  dir="o")),     # HD-HSYNC, Horizontal Sync
            Subsignal("int", Pins("U14",  dir="i")),     # HD-INT, Interupt signal
            Subsignal("spdifo", Pins("H20", dir="i")), # HD-SPDIFO, Sony/Philips audio out
            Subsignal("yuv", Pins("AB21 AA21 AB22 AA22 V19 V18 V20 U20 W21 W20 W18 T19 U19 R19 T17 T16", dir="o")),  # HD-D[15:0], Video Data in YCbCr 4:2:2 format
            Attrs(IOSTANDARD=bank_iostandard)
        ),

        *LEDResources(pins={
            19: "1",
            20: "2",
            21: "3",
            22: "3",
        }, conn=("pmod", 0), attrs=Attrs(IOSTANDARD=bank_iostandard)),

        *LEDResources(pins={
            18: "1",
            17: "2",
            16: "3",
            15: "3",
        }, conn=("pmod", 1), attrs=Attrs(IOSTANDARD=bank_iostandard)),

        *ButtonResources(pins={0: "G19", 1: "F19"},
                         attrs=Attrs(IO_STANDARD=bank_iostandard)),

        # User DIP Switches
        *SwitchResources(pins={
            0: "W6",   # SW0
            1: "W7",   # SW1
        }, attrs=Attrs(IOSTANDARD=bank_iostandard)),
    ]

    connectors = [
                             #J1  J2  J3  J4      J7   J8   J9  J10
        Connector("pmod", 0, "E15 D15 W17 W5  - - - - - - - -"),
        Connector("pmod", 1, "V7  W10 P18 P17 - - - - - - - -"),

        # FMC1 (J3)
        Connector("fmc", 0, {
            ## C
            "LA06_P": "J18", # C10
            "LA06_N": "K18", # C11
            "LA10_P": "L17", # C14
            "LA10_N": "M17", # C15
            "LA14_P": "J16", # C18
            "LA14_N": "J17", # C19
            "LA18_CC_P": "D20", # C22
            "LA18_CC_N": "C20", # C23
            "LA27_P": "C17", # C26
            "LA27_N": "C18", # C27

            # D
            "LA00_CC_P": "N19", # D8
            "LA01_CC_N": "N20", # D9
            "LA05_P": "N17", # D11
            "LA05_N": "N18", # D12
            "LA09_P": "M15", # D14
            "LA09_N": "M16", # D15
            "LA13_P": "P16", # D17
            "LA13_N": "R16", # D18
            "LA17_CC_P": "B19", # D20
            "LA17_CC_N": "B20", # D21
            "LA23_P": "G15", # D23
            "LA23_N": "G16", # D24
            "LA26_P": "F18", # D26
            "LA26_N": "E18", # D27

            # G
            "CLK1_P": "M19", # G2
            "CLK1_N": "M20", # G3
            "LA00_CC_P": "K19", # G6
            "LA00_CC_N": "K20", # G7
            "LA03_P": "J20", # G9
            "LA03_N": "K21", # G10
            "LA08_P": "J21", # G12
            "LA08_N": "J22", # G13
            "LA12_P": "N22", # G15
            "LA12_N": "P22", # G16
            "LA16_P": "N15", # G18
            "LA16_N": "P15", # G19
            "LA20_P": "G20", # G21
            "LA20_N": "G21", # G22
            "LA22_P": "G17", # G24
            "LA22_N": "F17", # G25
            "LA25_P": "C15", # G27
            "LA25_N": "B15", # G28
            "LA29_P": "B16", # G30
            "LA29_N": "B17", # G31
            "LA31_P": "A16", # G33
            "LA31_N": "A17", # G34
            "LA33_P": "A18", # G36
            "LA33_N": "A19", # G37

            # H
            "CLK0_P": "L18", # H4
            "CLK0_N": "L19", # H5
            "LA02_P": "L21", # H7
            "LA02_N": "L22", # H8
            "LA04_P": "M21", # H10
            "LA04_N": "M22", # H11
            "LA07_P": "J15", # H13
            "LA07_N": "K15", # H14
            "LA11_P": "R20", # H16
            "LA11_N": "R21", # H17
            "LA15_P": "P20", # H19
            "LA15_N": "P21", # H20
            "LA19_P": "E19", # H22
            "LA19_N": "E20", # H23
            "LA21_P": "F21", # H25
            "LA21_N": "F22", # H26
            "LA24_P": "A21", # H28
            "LA24_N": "A22", # H29
            "LA28_P": "D22", # H31
            "LA28_N": "C22", # H32
            "LA30_P": "E21", # H34
            "LA30_N": "D21", # H35
            "LA32_P": "B21", # H37
            "LA32_N": "B22", # H38
        }),

        # FMC2 (J4)
        Connector("fmc", 1, {
            ## C
            "LA06_P": "U17", # C10
            "LA06_N": "V17", # C11
            "LA10_P": "Y20", # C14
            "LA10_N": "Y21", # C15
            "LA14_P": "T22", # C18
            "LA14_N": "U22", # C19
            "LA18_CC_P": "AA9", # C22
            "LA18_CC_N": "AA8", # C23
            "LA27_P": "AB2", # C26
            "LA27_N": "AB1", # C27

            # D
            "LA00_CC_P": "W16", # D8
            "LA01_CC_N": "Y16", # D9
            "LA05_P": "AB19", # D11
            "LA05_N": "AB20", # D12
            "LA09_P": "U15", # D14
            "LA09_N": "U16", # D15
            "LA13_P": "V22", # D17
            "LA13_N": "W22", # D18
            "LA17_CC_P": "AA7", # D20
            "LA17_CC_N": "AA6", # D21
            "LA23_P": "V12", # D23
            "LA23_N": "W12", # D24
            "LA26_P": "U12", # D26
            "LA26_N": "U11", # D27

            # G
            "CLK1_P": "Y6", # G2
            "CLK1_N": "Y5", # G3
            "LA00_CC_P": "Y19", # G6
            "LA00_CC_N": "AA19", # G7
            "LA03_P": "AA16", # G9
            "LA03_N": "AB16", # G10
            "LA08_P": "AA17", # G12
            "LA08_N": "AB17", # G13
            "LA12_P": "W15", # G15
            "LA12_N": "Y15", # G16
            "LA16_P": "AB14", # G18
            "LA16_N": "AB15", # G19
            "LA20_P": "T4", # G21
            "LA20_N": "U4", # G22
            "LA22_P": "U10", # G24
            "LA22_N": "U9", # G25
            "LA25_P": "AA12", # G27
            "LA25_N": "AB12", # G28
            "LA29_P": "AA11", # G30
            "LA29_N": "AB11", # G31
            "LA31_P": "AB10", # G33
            "LA31_N": "AB9", # G34
            "LA33_P": "Y11", # G36
            "LA33_N": "Y10", # G37

            # H
            "CLK0_P": "Y18", # H4
            "CLK0_N": "AA18", # H5
            "LA02_P": "V14", # H7
            "LA02_N": "V15", # H8
            "LA04_P": "V13", # H10
            "LA04_N": "W13", # H11
            "LA07_P": "T21", # H13
            "LA07_N": "U21", # H14
            "LA11_P": "Y14", # H16
            "LA11_N": "AA14", # H17
            "LA15_P": "Y13", # H19
            "LA15_N": "AA13", # H20
            "LA19_P": "R6", # H22
            "LA19_N": "T6", # H23
            "LA21_P": "V5", # H25
            "LA21_N": "V4", # H26
            "LA24_P": "U6", # H28
            "LA24_N": "U5", # H29
            "LA28_P": "AB5", # H31
            "LA28_N": "AB4", # H32
            "LA30_P": "AB7", # H34
            "LA30_N": "AB6", # H35
            "LA32_P": "Y4", # H37
            "LA32_N": "AA4", # H38
        }),

        # TODO: XADC
    ]
