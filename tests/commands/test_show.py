"""Tests for the 'show' command."""

import unittest.mock as mock

import pytest

from localalias import commands
from localalias import errors


def test_show(capsys, cleandir, fake_db, show_cmd):
    """Tests show command."""
    show_cmd()
    captured = capsys.readouterr()
    assert captured.out == show_cmd.expected


def test_show_all(capsys, cleandir, _show_expected, fake_db):
    """Tests show command when no specific alias is provided."""
    show_cmd = commands.Show(None, color=False)
    show_cmd()
    expected = '{0}{1}\n{2}'.format(_show_expected['T'],
                                    _show_expected['TT'],
                                    _show_expected['multiline'])
    captured = capsys.readouterr()
    assert captured.out == expected


def test_show_failure(cleandir, show_cmd):
    """Tests show command fails properly when no local alias database exists."""
    with pytest.raises(errors.AliasNotDefinedError):
        show_cmd()


@pytest.fixture
def show_cmd(args, show_expected):
    """Builds and returns show command."""
    cmd = commands.Show(args.alias, cmd_args=args.cmd_args, color=args.color)
    cmd.expected = show_expected[args.alias]
    return cmd


@pytest.fixture
def show_expected(_show_expected):
    """Expected results for show command tests."""
    show_expected = {
        'T': '{}{}'.format(_show_expected['T'], _show_expected['TT']),  # example of prefix matching
        'TT': _show_expected['TT'],
        'multiline': _show_expected['multiline']
    }

    return show_expected


@pytest.fixture
def _show_expected(alias_dict):
    """Expected results for show command tests BEFORE prefix matching feature was added."""
    show_expected = {
        'T': 'T() {{ {0}; }}\n'.format(alias_dict['T']),
        'TT': 'TT() {{ {0}; }}\n'.format(alias_dict['TT']),
        'multiline': 'multiline() {{\n\t{0}\n}}\n'.format(alias_dict['multiline'].replace('\n', '\n\t'))
    }

    return show_expected
