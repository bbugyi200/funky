"""Tests command functionality."""

import unittest.mock as mock

import pytest

from localalias import commands

pytestmark = pytest.mark.usefixtures("debug_mode")


@pytest.fixture
def show_cmd(cmd_args):
    """Builds and returns show command."""
    show_cmd = commands.Show(cmd_args.alias, color=cmd_args.color)
    show_cmd.expected = cmd_args.expected
    return show_cmd


def test_show_command(capsys, cleandir, local_db, show_cmd):
    """Tests show command."""
    show_cmd()
    captured = capsys.readouterr()
    assert captured.out == show_cmd.expected


def test_show_command_failure(cleandir, show_cmd):
    """Tests show command fails properly when no local alias database exists."""
    with pytest.raises(RuntimeError):
        show_cmd()
