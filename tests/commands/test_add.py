"""Tests for the 'add' command."""

import json
import unittest.mock as mock

import pytest

from funky import commands
from funky import errors
import shared


@mock.patch('funky.commands.tempfile')
@mock.patch('funky.commands.sp')
def test_add(sp, tempfile, setup_edit_patches, cleandir, add_cmd, funk_dict):
    """Tests add command."""
    funk_cmd_string = funk_dict[add_cmd.funk]
    setup_edit_patches(sp, tempfile, funk_cmd_string)
    add_cmd()

    loaded_funks = shared.load_funks()
    assert loaded_funks == {add_cmd.funk: funk_cmd_string}
    assert len(loaded_funks) == 1


@mock.patch('funky.commands.tempfile')
@mock.patch('funky.commands.sp')
def test_add_empty(sp, tempfile, setup_edit_patches, cleandir):
    """Tests that add command does NOT accept empty funk definitions."""
    funk_cmd_string = ''
    setup_edit_patches(sp, tempfile, funk_cmd_string)

    with pytest.raises(errors.FunkyError):
        cmd = commands.Add(['new_funk'])
        cmd()


@pytest.fixture
def add_cmd(args):
    """Builds and returns 'add' command."""
    cmd = commands.Add(args.args, color=args.color)
    return cmd
