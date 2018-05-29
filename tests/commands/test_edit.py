"""Tests for edit command."""

import json
import unittest.mock as mock

import pytest

from localalias import commands
import shared


@pytest.fixture
def edit_cmd(args):
    """Builds and returns 'edit' command."""
    cmd = commands.Edit(args)
    return cmd


@mock.patch('localalias.commands.Edit.edit_alias')
def test_edit(edit_alias, cleandir, fake_db, edit_cmd):
    """Tests edit command."""
    edited_cmd_string = 'TEST COMMAND STRING'
    edit_alias.return_value = edited_cmd_string
    edit_cmd()
    loaded_aliases = shared.load_aliases()
    assert loaded_aliases[edit_cmd.args.alias] == edited_cmd_string


@mock.patch('localalias.commands.Edit.edit_alias')
def test_edit_all(edit_alias, cleandir, fake_db, alias_dict):
    """Tests edit command when no specific alias is given."""
    def new_cmd_string(old):
        return '{}: Edited Command String'.format(old)

    edit_alias.side_effect = new_cmd_string
    edit_cmd = commands.Edit(shared.build_args(None))
    edit_cmd()

    loaded_aliases = shared.load_aliases()
    for alias in alias_dict:
        assert loaded_aliases[alias] == new_cmd_string(alias)
