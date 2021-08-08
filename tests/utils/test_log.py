"""Tests the funky.utils.log utilities."""

import logging
import os
from pathlib import Path

import pytest

from funky.utils import log


@pytest.mark.parametrize("debug", [False, True])
def test_init_logger(debug: bool) -> None:
    """Tests that loggers are initialized properly."""
    log.init_logger(debug=debug)
    assert log.logger.isEnabledFor(logging.DEBUG) == debug


def test_logfile(xdg_data_home: Path) -> None:
    """Tests that the debugging logfile is working correctly."""
    log.init_logger(debug=True)
    log.logger.debug("TEST")
    logfile = f"{xdg_data_home}/funky/debug.log"
    assert os.path.isfile(logfile)
    with open(logfile, "r") as f:
        assert "TEST" in f.read()

    os.remove(logfile)
