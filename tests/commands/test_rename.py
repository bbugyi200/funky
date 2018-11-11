"""Tests for rename command."""

import unittest.mock as mock

import pytest

from funky import commands
from funky import errors
import shared


def test_rename(cleandir, fake_db, rename_cmd, funk_dict):
    """Test rename command."""
    old_cmd_string = funk_dict[rename_cmd.funk]
    rename_cmd()
    loaded_funks = shared.load_funks()
    assert loaded_funks[rename_cmd.args[0]] == old_cmd_string


def test_rename_fail(cleandir, fake_db):
    """Test that rename command fails when OLD funk does not exist."""
    cmd = commands.Rename(['bad_funk', 'NEW'])
    with pytest.raises(errors.FunkNotDefinedError):
        cmd()


@pytest.fixture
def rename_cmd(args):
    """Builds and returns 'rename' command"""
    cmd = commands.Rename([args.args[0], 'NEW'])
    return cmd


@pytest.mark.parametrize('y_or_n', ['y', 'n'])
@mock.patch('funky.utils.getch')
def test_rename_overwrite(getch, y_or_n, cleandir, fake_db, funk_dict):
    """Test that rename overwrites existing function names properly."""
    getch.side_effect = lambda x: y_or_n
    fnames = [name for name in funk_dict]
    OLD, NEW = fnames[0], fnames[1]
    cmd = commands.Rename([OLD, NEW])
    cmd()

    loaded_funks = shared.load_funks()
    if y_or_n == "y":
        cmd_string = funk_dict[OLD]
    else:
        cmd_string = funk_dict[NEW]

    assert loaded_funks[NEW] == cmd_string
