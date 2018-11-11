"""Tests for remove command."""

import json
import os
import unittest.mock as mock

import pytest

from funky import commands
import shared


def test_remove(cleandir, fake_db, remove_cmd):
    """Tests remove command."""
    remove_cmd()
    loaded_funks = shared.load_funks()
    assert remove_cmd.funk not in loaded_funks


@pytest.fixture
def remove_cmd(args):
    """Builds and returns 'remove' command."""
    cmd = commands.Remove(args.args, color=args.color)
    return cmd


def test_remove_last(cleandir, funk_dict, fake_db):
    """Tests that local funk database is removed when last funk is removed."""
    assert os.path.isfile(commands.Command.FUNKY_DB_FILENAME)

    for funk in funk_dict:
        remove_cmd = commands.Remove(funk)
        remove_cmd()

    assert not os.path.isfile(commands.Command.FUNKY_DB_FILENAME)


@pytest.mark.parametrize('y_or_n', ['y', 'n'])
@mock.patch('funky.utils.getch')
def test_remove_all(getch, y_or_n, cleandir, fake_db):
    """Tests that the local funk database is removed when no funk is provided and the
    user confirms.
    """
    getch.side_effect = lambda x: y_or_n

    assert os.path.isfile(commands.Command.FUNKY_DB_FILENAME)

    remove_cmd = commands.Remove(None)
    remove_cmd()

    isfile = os.path.isfile(commands.Command.FUNKY_DB_FILENAME)
    if y_or_n == 'y':
        expected = not isfile
    else:
        expected = isfile

    assert expected
