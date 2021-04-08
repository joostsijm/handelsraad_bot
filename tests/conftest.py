"""Test configuration"""

import pytest
import _pytest.skipping
from dotenv import load_dotenv

load_dotenv()


def pytest_addoption(parser):
    """Add option to parser to prevent skips"""
    parser.addoption(
        "--no-skips",
        action="store_true",
        default=False, help="disable skip marks")


@pytest.hookimpl(tryfirst=True)
def pytest_cmdline_preparse(config, args):
    """Add check for skips"""
    if "--no-skips" not in args:
        return

    def no_skip(*args, **kwargs):
        return

    _pytest.skipping.skip = no_skip


@pytest.fixture(scope='module')
def vcr(vcr):
    """Set parameters vor VCR"""
    vcr.ignore_localhost = True
    return vcr
