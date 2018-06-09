"""Tests for rename command."""

import unittest.mock as mock

import pytest

from localalias import commands
from localalias import errors
import shared


def test_rename(cleandir, fake_db, rename_cmd, alias_dict):
    """Tests rename command."""
    old_cmd_string = alias_dict[rename_cmd.alias]
    rename_cmd()
    loaded_aliases = shared.load_aliases()
    assert loaded_aliases[rename_cmd.args[0]] == old_cmd_string


def test_rename_fail(cleandir, fake_db):
    """Tests that rename command fails when OLD alias does not exist."""
    cmd = commands.Rename(['bad_alias', 'NEW'])
    with pytest.raises(errors.AliasNotDefinedError):
        cmd()


@pytest.fixture
def rename_cmd(args):
    """Builds and returns 'rename' command"""
    cmd = commands.Rename([args.args[0], 'NEW'])
    return cmd
