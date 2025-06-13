#

from amaranth.vendor import XilinxPlatform

class ZynqPlatform(XilinxPlatform):
    def __init__(self, bif=None):
        self._bif = bif
        super().__init__()

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
