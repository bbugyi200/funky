"""Tests for the 'add' command."""

import json
import unittest.mock as mock

import pytest

from localalias import commands
import shared


@mock.patch('localalias.commands.tempfile')
@mock.patch('localalias.commands.sp')
def test_add(sp, tempfile, setup_edit_patches, cleandir, add_cmd, alias_dict):
    """Tests add command."""
    alias_cmd_string = alias_dict[add_cmd.alias]
    setup_edit_patches(sp, tempfile, alias_cmd_string)
    add_cmd()

    loaded_aliases = shared.load_aliases()
    assert loaded_aliases == {add_cmd.alias: alias_cmd_string}
    assert len(loaded_aliases) == 1


@pytest.fixture
def add_cmd(args):
    """Builds and returns 'add' command."""
    cmd = commands.Add(args.args, color=args.color)
    return cmd
