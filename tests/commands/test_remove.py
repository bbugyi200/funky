"""Tests for remove command."""

import json
import os
import unittest.mock as mock

import pytest

from localalias import commands
import shared


@pytest.fixture
def remove_cmd(args):
    """Builds and returns 'remove' command."""
    cmd = commands.Remove(args)
    return cmd


def test_remove(cleandir, fake_db, remove_cmd):
    """Tests remove command."""
    remove_cmd()
    loaded_aliases = shared.load_aliases()
    assert remove_cmd.args.alias not in loaded_aliases


def test_remove_last(cleandir, alias_dict, fake_db):
    """Tests that local alias database is removed when last alias is removed."""
    assert os.path.isfile(commands.Command.LOCALALIAS_DB_FILENAME)

    for alias in alias_dict:
        remove_cmd = commands.Remove(shared.build_args(alias))
        remove_cmd()

    assert not os.path.isfile(commands.Command.LOCALALIAS_DB_FILENAME)


@mock.patch('localalias.utils.getch')
def test_remove_all(getch, cleandir, fake_db):
    """Tests that the local alias database is removed when no alias is provided and the
    user confirms.
    """
    getch.side_effect = lambda x: 'y'

    assert os.path.isfile(commands.Command.LOCALALIAS_DB_FILENAME)

    remove_cmd = commands.Remove(shared.build_args(None))
    remove_cmd()

    assert not os.path.isfile(commands.Command.LOCALALIAS_DB_FILENAME)
