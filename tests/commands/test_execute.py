"""Tests for execute command."""

import unittest.mock as mock

import pytest

from localalias import commands

pytestmark = pytest.mark.usefixtures("debug_mode")


@pytest.fixture
def execute_cmd(cmd_args):
    """Builds and returns execute command."""
    cmd = commands.Execute(cmd_args.alias, color=cmd_args.color)
    return cmd


@mock.patch('localalias.commands.sp')
def test_execute(subprocess, cleandir, fake_db, execute_cmd):
    """Tests execute command."""
    subprocess.call = mock.Mock()
    execute_cmd()
    subprocess.call.assert_called_once_with(['zsh', '-c', execute_cmd.alias_dict[execute_cmd.alias]])
