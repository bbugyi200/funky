"""Tests for main application (entry point)."""

import argparse
import unittest.mock as mock

import pytest

from localalias import app


@pytest.mark.parametrize('argv,action,lalias,debug', [
    (['-a', 'new_alias', '--debug'], app.Action.ADD, 'new_alias', True),
    (['--show'], app.Action.SHOW, None, False),
    (['--remove', 'new_alias', '-d'], app.Action.REMOVE, 'new_alias', True)
])
@mock.patch('localalias.app._run')
def test_main(run,argv,action,lalias,debug):
    """Tests that arguments are parsed correctly."""
    app.main(argv)
    run.assert_called_once_with(argparse.Namespace(lalias=lalias, action=action, debug=debug))


@pytest.mark.parametrize('argv', [['-a'], ['-x'], ['-r']])
def test_main_failure(argv):
    """Tests that bad arguments raise a ValueError."""
    with pytest.raises(ValueError):
        app.main(argv)
