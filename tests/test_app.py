"""Tests for main application (entry point)."""

import argparse
import unittest.mock as mock

import pytest

from localalias import app


@pytest.mark.parametrize('argv,action,debug,alias', [
    (['-a', '--debug', 'new_alias'], app._Actions.ADD, True, 'new_alias'),
    (['--show'], app._Actions.SHOW, False, None),
    (['--remove', '-d', 'new_alias'], app._Actions.REMOVE, True, 'new_alias')
])
@mock.patch('localalias.app._Actions.cmd_map')
def test_main(cmd_map, argv, action, debug, alias):
    """Tests that arguments are parsed correctly."""
    cmd_map.return_value = mock.Mock()
    app.main(argv)
    cmd_map.assert_called_once_with(argparse.Namespace(alias=alias, cmd_args=[], color=False, action=action, debug=debug))


@pytest.mark.parametrize('argv', [['-a'], ['-x']])
@mock.patch('localalias.utils.log.logger')
def test_main_failure(logger, argv):
    """Tests that bad arguments result in a nonzero exit status."""
    assert app.main(argv) == 1
    logger.error.called_once()
