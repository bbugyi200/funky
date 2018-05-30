"""Tests the localalias.utils.log utilities."""

import getpass
import logging
import os
import unittest.mock as mock

import pytest

import localalias.utils.log as log


@pytest.mark.parametrize('debug', [False, True])
def test_init_logger(debug):
    """Tests that loggers are initialized properly."""
    log.init_logger(debug=debug)
    assert log.logger.isEnabledFor(logging.DEBUG) == debug


def test_silence_streams():
    """Tests the log.silence_streams function.

    It is necessary to first cleanup any old handlers that might have been left over
    from previous tests.
    """
    root = logging.getLogger()
    handlers = []
    for handler in root.handlers:
        handlers.append(handler)

    for handler in handlers:
        root.removeHandler(handler)

    log.init_logger(debug=False)
    for handler in root.handlers:
        if isinstance(handler, logging.StreamHandler):
            assert handler.level == logging.INFO


def test_logfile():
    """Tests that the debugging logfile is working correctly."""
    log.init_logger(debug=True)
    log.logger.debug('TEST')
    logfile = '/home/{}/.local/share/localalias/debug.log'.format(getpass.getuser())
    assert os.path.isfile(logfile)
    with open(logfile, 'r') as f:
        assert 'TEST' in f.read()

    os.remove(logfile)
