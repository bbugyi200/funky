"""Tests for edit command."""

import json
import unittest.mock as mock

import pytest

from localalias import commands


@pytest.fixture
def edit_cmd(cmd_args):
    """Builds and returns 'edit' command."""
    cmd = commands.Edit(cmd_args.alias, color=cmd_args.color)
    return cmd


@mock.patch('localalias.commands.Edit.edit_alias')
def test_edit(edit_alias, cleandir, fake_db, edit_cmd):
    edited_cmd_string = 'TEST COMMAND STRING'
    edit_alias.return_value = edited_cmd_string
    edit_cmd()

    # loads aliases from database file
    with open(commands.Command.LOCALALIAS_DB_FILENAME, 'r') as f:
        loaded_aliases = json.load(f)

    assert loaded_aliases[edit_cmd.alias] == edited_cmd_string
