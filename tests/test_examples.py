#!/usr/bin/julia

from transactron import TransactronContextElaboratable

from amaranth_zynq.platform import ZedboardPlatform, ZC702Platform

from pathlib import Path
import importlib.util

import pytest

example_dir = Path(__file__).parent.parent / 'examples'

def load_example(name):
    spec = importlib.util.spec_from_file_location("example", example_dir / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("Platform", [ZedboardPlatform, ZC702Platform])
def test_axi7(Platform):
    m = load_example('axi7')
    core = TransactronContextElaboratable(m.AXIExample())
    plat = Platform()
    plat.build(core, do_build=False)

def test_axi():
    m = load_example('axi')
    core = TransactronContextElaboratable(m.AXIExample())
    plat = m.Zu3egPlatform()
    plat.build(core, do_build=False)

def test_basic():
    m = load_example('basic')
    core = m.BasicExample()
    plat = m.Zu3egPlatform()
    plat.build(core, do_build=False)

def test_zedboard():
    m = load_example('zedboard')
    core = m.Zedboard()
    plat = ZedboardPlatform()
    plat.build(core, do_build=False)
