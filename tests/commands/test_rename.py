"""Tests for rename command."""

import unittest.mock as mock

import pytest

from localalias import commands
from localalias import errors
import shared


def test_rename(cleandir, fake_db, rename_cmd, alias_dict):
    """Test rename command."""
    old_cmd_string = alias_dict[rename_cmd.alias]
    rename_cmd()
    loaded_aliases = shared.load_aliases()
    assert loaded_aliases[rename_cmd.args[0]] == old_cmd_string


def test_rename_fail(cleandir, fake_db):
    """Test that rename command fails when OLD alias does not exist."""
    cmd = commands.Rename(['bad_alias', 'NEW'])
    with pytest.raises(errors.AliasNotDefinedError):
        cmd()


@pytest.fixture
def rename_cmd(args):
    """Builds and returns 'rename' command"""
    cmd = commands.Rename([args.args[0], 'NEW'])
    return cmd


@pytest.mark.parametrize('y_or_n', ['y', 'n'])
@mock.patch('localalias.utils.getch')
def test_rename_overwrite(getch, y_or_n, cleandir, fake_db, alias_dict):
    """Test that rename overwrites existing function names properly."""
    getch.side_effect = lambda x: y_or_n
    fnames = [name for name in alias_dict]
    OLD, NEW = fnames[0], fnames[1]
    cmd = commands.Rename([OLD, NEW])
    cmd()

    loaded_aliases = shared.load_aliases()
    if y_or_n == "y":
        cmd_string = alias_dict[OLD]
    else:
        cmd_string = alias_dict[NEW]

    assert loaded_aliases[NEW] == cmd_string
