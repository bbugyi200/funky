"""Tests for edit command."""

import json
import unittest.mock as mock

import pytest

from localalias import commands
import shared


@mock.patch('localalias.commands.tempfile')
@mock.patch('localalias.commands.sp')
def test_edit(sp, tempfile, setup_edit_patches, cleandir, fake_db, edit_cmd):
    """Tests edit command."""
    edited_cmd_string = 'TEST COMMAND STRING'
    setup_edit_patches(sp, tempfile, edited_cmd_string)

    edit_cmd()

    loaded_aliases = shared.load_aliases()
    assert loaded_aliases[edit_cmd.alias] == '{} "$@"'.format(edited_cmd_string)


@mock.patch('localalias.commands.tempfile')
@mock.patch('localalias.commands.sp')
@mock.patch('localalias.commands.Edit.remove_alias')
def test_edit_empty(remove_alias, sp, tempfile, setup_edit_patches, cleandir, fake_db, alias_dict):
    """Tests that an alias definition left empty results in the alias being removed."""
    edited_cmd_string = ''
    setup_edit_patches(sp, tempfile, edited_cmd_string)

    some_alias = list(alias_dict.keys())[0]
    cmd = commands.Edit([some_alias])
    cmd()

    remove_alias.assert_called_once()


@pytest.fixture
def edit_cmd(args):
    """Builds and returns 'edit' command."""
    cmd = commands.Edit(args.args, color=args.color)
    return cmd


@mock.patch('localalias.commands.tempfile')
@mock.patch('localalias.commands.sp')
def test_edit_format(sp, tempfile, setup_edit_patches, cleandir, fake_db, alias_dict):
    """Tests that the edit command reformats command strings when needed."""
    edited_cmd_string = 'EDITED CMD STRING'

    setup_edit_patches(sp, tempfile, edited_cmd_string)

    some_alias = list(alias_dict.keys())[0]
    cmd = commands.Edit([some_alias])
    cmd()

    loaded_aliases = shared.load_aliases()
    assert loaded_aliases[some_alias] == '{} "$@"'.format(edited_cmd_string)
