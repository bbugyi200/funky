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


def test_show_prefix(capsys, cleandir, fake_db, show_expected):
    """Tests show command when funk prefix is used."""
    cmd = commands.Show('T..')
    cmd()
    captured = capsys.readouterr()
    assert captured.out == '{}{}'.format(show_expected['T'], show_expected['TT'])


def test_show_verbose(capsys, cleandir, fake_db, alias_dict):
    """Tests show command with verbose output."""
    cmd = commands.Show(None, verbose=True)
    cmd()
    captured = capsys.readouterr()

    count_no_newlines = 0
    for cmd_string in alias_dict.values():
        if '\n' not in cmd_string:
            count_no_newlines += 1

    assert captured.out.count('unalias') == len(alias_dict)
    assert captured.out.count('compdef') == count_no_newlines


def test_show_all(capsys, cleandir, show_expected, fake_db):
    """Tests show command when no specific alias is provided."""
    show_cmd = commands.Show(None, color=False)
    show_cmd()
    expected = '{0}{1}{2}'.format(
        show_expected['multiline'],
        show_expected['T'],
        show_expected['TT'],
    )
    captured = capsys.readouterr()
    assert captured.out == expected


def test_show_failure(cleandir, show_cmd):
    """Tests show command fails properly when no local alias database exists."""
    with pytest.raises(errors.AliasNotDefinedError):
        show_cmd()


@pytest.fixture
def show_cmd(args, show_expected):
    """Builds and returns show command."""
    cmd = commands.Show(args.args, color=args.color)
    cmd.expected = show_expected[args.args[0]]
    return cmd


@pytest.fixture
def show_expected(alias_dict):
    """Expected results for show command tests BEFORE prefix matching feature was added."""
    show_expected = {
        'T': 'T() {{ {0}; }}\n'.format(alias_dict['T']),
        'TT': 'TT() {{ {0}; }}\n'.format(alias_dict['TT']),
        'multiline': 'multiline() {{\n\t{0}\n}}\n'.format(alias_dict['multiline'].replace('\n', '\n\t'))
    }

    return show_expected
