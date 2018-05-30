"""Tests for execute command."""

import subprocess as sp
import unittest.mock as mock

import pytest

from localalias import commands


@mock.patch('localalias.commands.sp')
def test_execute(subprocess, cleandir, fake_db, execute_cmd):
    """Tests execute command."""
    subprocess.call = mock.Mock()
    execute_cmd()

    cmd_list = subprocess.call.call_args[0][0]
    cmd = cmd_list[-1]
    out = sp.check_output(['bash', '-c', cmd])
    assert out.decode().strip() == execute_cmd.expected


@pytest.fixture
def execute_cmd(args, execute_expected):
    """Builds and returns execute command."""
    cmd = commands.Execute(args.alias, cmd_args=args.cmd_args, color=args.color)
    expected = execute_expected[args.alias]

    if '$1' in expected:
        try:
            expected = expected.replace('$1', args.cmd_args[0])
        except IndexError as e:
            raise ValueError("The args.cmd_args array should not be nonempty when $1 exists in "
                             "test command string!")

    cmd.expected = expected
    return cmd


@pytest.fixture
def execute_expected(alias_dict):
    """Expected results for execute command tests."""
    execute_expected = {}
    for alias in alias_dict:
        expected = alias_dict[alias].replace('echo ', '').strip('"').replace('"\n"', '\n')
        execute_expected[alias] = expected

    return execute_expected
