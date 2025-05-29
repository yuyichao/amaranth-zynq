from amaranth.vendor import XilinxPlatform


class ZynqMPPlatform(XilinxPlatform):
    _vivado_file_templates = {
        **XilinxPlatform._vivado_file_templates,
        "{{name}}.bif": r"""
            all:
            {
                [destination_device = pl] {{name}}.bit
            }
        """
    }

    _vivado_command_templates = [
        *XilinxPlatform._vivado_command_templates,
        r"""
            bootgen
            -image {{name}}.bif
            -arch zynqmp
            -w
            -o {{name}}_bootgen.bin
        """
    ]
