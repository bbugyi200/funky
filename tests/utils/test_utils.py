"""Tests miscellaneous utilities."""

import mock

import pytest

from funky import utils


@mock.patch('funky.utils.core.tty')
@mock.patch('funky.utils.core.termios')
@mock.patch('funky.utils.core.sys.stdin.fileno')
@mock.patch('funky.utils.core.sys.stdin.read')
def test_getch(read, fileno, termios, tty, capsys):
    """Tests getch utility function.

    TODO: This test is clearly terrible. I need to figure out how to test utils.getch without
        patching every single module involved.
    """
    read.return_value = 'y'
    fileno.return_value = 0

    prompt = 'PROMPT: '
    assert utils.getch(prompt) == 'y'

    captured = capsys.readouterr()
    assert captured.out == prompt
