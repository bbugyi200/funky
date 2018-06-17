"""Tests for remove command."""

import json
import os
import unittest.mock as mock

import pytest

from localalias import commands
import shared


def test_remove(cleandir, fake_db, remove_cmd):
    """Tests remove command."""
    remove_cmd()
    loaded_aliases = shared.load_aliases()
    assert remove_cmd.alias not in loaded_aliases


@pytest.fixture
def remove_cmd(args):
    """Builds and returns 'remove' command."""
    cmd = commands.Remove(args.args, color=args.color)
    return cmd


def test_remove_last(cleandir, alias_dict, fake_db):
    """Tests that local alias database is removed when last alias is removed."""
    assert os.path.isfile(commands.Command.LOCALALIAS_DB_FILENAME)

    for alias in alias_dict:
        remove_cmd = commands.Remove(alias)
        remove_cmd()

    assert not os.path.isfile(commands.Command.LOCALALIAS_DB_FILENAME)


@pytest.mark.parametrize('y_or_n', ['y', 'n'])
@mock.patch('localalias.utils.getch')
def test_remove_all(getch, y_or_n, cleandir, fake_db):
    """Tests that the local alias database is removed when no alias is provided and the
    user confirms.
    """
    getch.side_effect = lambda x: y_or_n

    assert os.path.isfile(commands.Command.LOCALALIAS_DB_FILENAME)

    remove_cmd = commands.Remove(None)
    remove_cmd()

    isfile = os.path.isfile(commands.Command.LOCALALIAS_DB_FILENAME)
    if y_or_n == 'y':
        expected = not isfile
    else:
        expected = isfile

    assert expected
