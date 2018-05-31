"""Tests for execute command."""

import re
import subprocess as sp
import unittest.mock as mock

import pytest

from localalias import commands


@mock.patch('localalias.commands.sp')
@mock.patch('localalias.commands.sys.exit')
def test_execute(exit, subprocess, cleandir, fake_db, execute_cmd):
    """Tests execute command."""
    subprocess.call = mock.Mock()
    execute_cmd()

    cmd_list = subprocess.Popen.call_args[0][0]
    cmd = cmd_list[-1]
    out = sp.check_output(['bash', '-c', cmd])
    assert out.decode().strip() == execute_cmd.expected


@pytest.fixture
def execute_cmd(args, execute_expected):
    """Builds and returns execute command."""
    cmd = commands.Execute(args.alias, cmd_args=args.cmd_args, color=args.color)
    expected = execute_expected[args.alias]

    if '\n' not in expected:
        if '$1' in expected:
            try:
                expected = expected.replace('$1', args.cmd_args[0])
            except IndexError as e:
                raise RuntimeError('Not enough simulated command-line arguments.')
        elif any(x in expected for x in ['$@', '$*']):
            expected = expected.replace('$@', ' '.join(args.cmd_args))
            expected = expected.replace('$*', ' '.join(args.cmd_args))
        else:
            expected = '{} {}'.format(expected, ' '.join(args.cmd_args))

    cmd.expected = expected
    return cmd


@pytest.fixture
def execute_expected(alias_dict):
    """Expected results for execute command tests."""
    execute_expected = {}
    for alias in alias_dict:
        expected = alias_dict[alias].replace('echo ', '')
        execute_expected[alias] = expected

    return execute_expected
