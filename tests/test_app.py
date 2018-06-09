"""Tests for main application (entry point)."""

import argparse
import unittest.mock as mock

import pytest

from localalias import app
from localalias import errors


@pytest.mark.parametrize('argv,cmd_cls_string', [
    (['-a', 'new_alias'], 'Add'),
    (['-e', 'new_alias'], 'Edit'),
    (['-r', 'new_alias'], 'Remove'),
    (['-x', 't', '-x'], 'Execute'),
])
@mock.patch('localalias.app.commands')
def test_main(commands, argv, cmd_cls_string):
    """Tests that arguments are parsed correctly."""
    setattr(commands, cmd_cls_string, mock.Mock())
    cmd_class = getattr(commands, cmd_cls_string)
    app.main(argv)

    cmd_class.assert_called_once_with(argv[1:], color=False)
    app._CmdAction.flag = None


@mock.patch('localalias.utils.log.logger')
def test_main_failure(logger):
    """Tests that bad arguments result in a nonzero exit status."""
    assert app.main(['-a', 'new_alias', '-e', 'existing_alias']) == 1
    logger.error.called_once()


@mock.patch('localalias.app._get_argparser')
def test_main_exceptions(_get_argparser):
    """Tests that main handles exceptions appropriately."""
    class TestError(Exception):
        pass

    def raise_error(opt):
        if opt == 1:
            raise errors.LocalAliasError(returncode=5)
        elif opt == 2:
            raise TestError('Test Exception')

    _get_argparser.side_effect = lambda: raise_error(1)
    assert app.main() == 5

    _get_argparser.side_effect = lambda: raise_error(2)
    with pytest.raises(TestError):
        app.main()
