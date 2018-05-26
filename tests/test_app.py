"""Tests for main application (entry point)."""

import argparse
import unittest.mock as mock

import pytest

from localalias import app


@pytest.mark.parametrize('argv,action,lalias,debug', [
    (['-a', 'new_alias', '--debug'], app._Actions.ADD, 'new_alias', True),
    (['--show'], app._Actions.SHOW, None, False),
    (['--remove', 'new_alias', '-d'], app._Actions.REMOVE, 'new_alias', True)
])
@mock.patch('localalias.app._Actions.cmd_map')
def test_main(cmd_map,argv,action,lalias,debug):
    """Tests that arguments are parsed correctly."""
    cmd_map.return_value = (mock.Mock(), tuple(), dict())
    app.main(argv)
    cmd_map.assert_called_once_with(argparse.Namespace(lalias=lalias, action=action, debug=debug))


@pytest.mark.parametrize('argv', [['-a'], ['-x'], ['-r']])
@mock.patch('localalias.utils.log.logger')
def test_main_failure(logger,argv):
    """Tests that bad arguments raise a ValueError."""
    app.main(argv)
    logger.error.called_once()
