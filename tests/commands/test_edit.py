"""Tests for edit command."""

import json
import unittest.mock as mock

import pytest

from localalias import commands
import shared


@mock.patch('localalias.commands.Edit.edit_alias')
def test_edit(edit_alias, cleandir, fake_db, edit_cmd):
    """Tests edit command."""
    edited_cmd_string = 'TEST COMMAND STRING'
    edit_alias.return_value = edited_cmd_string
    edit_cmd()
    loaded_aliases = shared.load_aliases()
    assert loaded_aliases[edit_cmd.alias] == edited_cmd_string


@pytest.fixture
def edit_cmd(args):
    """Builds and returns 'edit' command."""
    cmd = commands.Edit(args.alias, cmd_args=args.cmd_args, color=args.color)
    return cmd


@mock.patch('localalias.commands.tempfile')
@mock.patch('localalias.commands.sp')
def test_edit_format(sp, tempfile, cleandir, fake_db, alias_dict):
    """Tests that the edit command reformats command strings when needed."""
    edited_cmd_string = 'EDITED CMD STRING'

    tmpfilename = '/tmp/test_edit_format.txt'
    with open(tmpfilename, 'w') as f:
        f.write(edited_cmd_string)

    fileMock = mock.Mock(name='fileMock')
    fileMock.name = tmpfilename
    tempfile.NamedTemporaryFile = mock.Mock()
    tempfile.NamedTemporaryFile.return_value = fileMock

    some_alias = list(alias_dict.keys())[0]
    edit_cmd = commands.Edit(some_alias)
    edit_cmd()

    loaded_aliases = shared.load_aliases()
    assert loaded_aliases[some_alias] == '{} $@'.format(edited_cmd_string)
