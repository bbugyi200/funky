"""Tests the localalias.utils.log utilities."""

import getpass
import logging
import os
import unittest.mock as mock

import pytest

import localalias.utils.log as log


@pytest.mark.parametrize('debug,HandlerTypes', [
    (False, logging.StreamHandler),
    (True, (logging.StreamHandler, logging.FileHandler))
])
def test_init_logger(debug,HandlerTypes):
    """Tests that logger handlers are initialized properly."""
    logger = mock.Mock()
    logger.handlers = []
    logger.addHandler = lambda h: logger.handlers.append(h)
    log.init_logger(logger, debug=debug)
    for handler in logger.handlers:
        assert isinstance(handler, HandlerTypes)


def test_logger():
    log.init_logger(log.logger, debug=True)
    log.logger.debug('TEST')
    logfile = '/home/{}/.local/share/localalias/debug.log'.format(getpass.getuser())
    assert os.path.isfile(logfile)
    with open(logfile, 'r') as f:
        assert 'TEST' in f.read()

    os.remove(logfile)
