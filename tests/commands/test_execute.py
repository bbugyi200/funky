"""Tests for execute command."""

import re
import subprocess as sp
import unittest.mock as mock

import pytest

from localalias import commands
from localalias import errors


@mock.patch('localalias.commands.sp')
@mock.patch('localalias.commands.sys.exit')
def test_execute(exit, subprocess, cleandir, fake_global_db, fake_db, execute_cmd):
    """Tests execute command.

    NOTE: fake_global_db is not used but including it among the listed fixtures ensures that local
          aliases take precedence over global ones.
    """
    subprocess.call = mock.Mock()
    execute_cmd()

    cmd_list = subprocess.Popen.call_args[0][0]
    cmd = cmd_list[-1]
    out = sp.check_output(['bash', '-c', cmd])
    assert out.decode().strip() == execute_cmd.expected


@mock.patch('localalias.commands.sys.exit')
def test_execute_global(exit, cleandir, global_filename, fake_global_db, global_alias_dict):
    """Tests global aliases

    NOTE: Unlike test_execute, this test merely tests whether the alias is found, NOT if it is
          executed properly.
    """
    commands.Command.GLOBALALIAS_DB_FILENAME = global_filename
    for alias in global_alias_dict:
        cmd = commands.Execute([alias])
        cmd()

    with pytest.raises(errors.AliasNotDefinedError):
        cmd = commands.Execute(['bad_alias'])
        cmd()


@pytest.fixture
def execute_cmd(args, execute_expected):
    """Builds and returns execute command."""
    cmd = commands.Execute(args.args, color=args.color)
    expected = execute_expected[args.args[0]]

    if '\n' not in expected:
        if '$1' in expected:
            try:
                expected = expected.replace('$1', args.args[1])
            except IndexError as e:
                raise RuntimeError('Not enough simulated command-line arguments.')
        elif any(x in expected for x in ['$@', '$*']):
            expected = expected.replace('$@', ' '.join(args.args[1:]))
            expected = expected.replace('$*', ' '.join(args.args[1:]))
        else:
            expected = '{} {}'.format(expected, ' '.join(args.args[1:]))

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
