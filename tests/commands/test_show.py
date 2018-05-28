"""Tests for the 'show' command."""

import unittest.mock as mock

import pytest

from localalias import commands

pytestmark = pytest.mark.usefixtures("debug_mode")


@pytest.fixture
def show_expected(alias_dict):
    show_expected = {
        'run': 'run() {{ {0}; }}\n'.format(alias_dict['run']),
        'T': 'T() {{ {0}; }}\n'.format(alias_dict['T']),
        'multiline': 'multiline() {{\n\t{0}\n}}\n'.format(alias_dict['multiline'].replace('\n', '\n\t'))
    }

    return show_expected


@pytest.fixture
def show_cmd(cmd_args, show_expected):
    """Builds and returns show command."""
    cmd = commands.Show(cmd_args.alias, color=cmd_args.color)
    cmd.expected = show_expected[cmd_args.alias]
    return cmd


def test_show(capsys, cleandir, fake_db, show_cmd):
    """Tests show command."""
    show_cmd()
    captured = capsys.readouterr()
    assert captured.out == show_cmd.expected


def test_show_none(capsys, cleandir, show_expected, fake_db):
    show_cmd = commands.Show(None, color=False)
    show_cmd()
    expected = '{0}\n{1}\n{2}'.format(show_expected['T'],
                                      show_expected['multiline'],
                                      show_expected['run'])
    captured = capsys.readouterr()
    assert captured.out == expected


def test_show_failure(cleandir, show_cmd):
    """Tests show command fails properly when no local alias database exists."""
    with pytest.raises(RuntimeError):
        show_cmd()
