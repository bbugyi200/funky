"""Tests for edit command."""

import json
import os
import unittest.mock as mock

import pytest

from funky import commands
import shared


@mock.patch('funky.commands.tempfile')
@mock.patch('funky.commands.sp')
def test_edit(sp, tempfile, setup_edit_patches, cleandir, fake_db, edit_cmd):
    """Tests edit command."""
    edited_cmd_string = 'TEST COMMAND STRING'
    setup_edit_patches(sp, tempfile, edited_cmd_string)

    edit_cmd()

    loaded_funks = shared.load_funks()
    assert loaded_funks[edit_cmd.funk] == '{} "$@"'.format(edited_cmd_string)


@mock.patch('funky.commands.tempfile')
@mock.patch('funky.commands.sp')
def test_edit_empty(sp, tempfile, setup_edit_patches, cleandir, fake_db, funk_dict):
    """Tests that a funk definition left empty results in the funk being removed.

    This function also tests that the funky database is deleted after all local funks have
    been removed.
    """
    edited_cmd_string = ''

    assert os.path.isfile(commands.Command.FUNKY_DB_FILENAME)

    for i, funk in enumerate(funk_dict):
        setup_edit_patches(sp, tempfile, edited_cmd_string)
        cmd = commands.Edit([funk])
        assert len(cmd.funk_dict) == (len(funk_dict) - i)
        cmd()

    assert not os.path.isfile(commands.Command.FUNKY_DB_FILENAME)


@pytest.fixture
def edit_cmd(args):
    """Builds and returns 'edit' command."""
    cmd = commands.Edit(args.args, color=args.color)
    return cmd


@mock.patch('funky.commands.tempfile')
@mock.patch('funky.commands.sp')
def test_edit_format(sp, tempfile, setup_edit_patches, cleandir, fake_db, funk_dict):
    """Tests that the edit command reformats command strings when needed."""
    edited_cmd_string = 'EDITED CMD STRING'

    setup_edit_patches(sp, tempfile, edited_cmd_string)

    some_funk = list(funk_dict.keys())[0]
    cmd = commands.Edit([some_funk])
    cmd()

    loaded_funks = shared.load_funks()
    assert loaded_funks[some_funk] == '{} "$@"'.format(edited_cmd_string)
