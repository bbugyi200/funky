"""Tests miscellaneous utilities."""

import mock
import pytest  # pylint: disable=unused-import

from funky import utils


@mock.patch("funky.utils.tty")
@mock.patch("funky.utils.termios")
@mock.patch("funky.utils.sys.stdin.fileno")
@mock.patch("funky.utils.sys.stdin.read")
def test_getch(read, fileno, _, __, capsys):
    """Tests getch utility function.

    TODO: This test is clearly terrible. I need to figure out how to test
          utils.getch without patching every single module involved.
    """
    read.return_value = "y"
    fileno.return_value = 0

    prompt = "PROMPT: "
    assert utils.getch(prompt) == "y"

    captured = capsys.readouterr()
    assert captured.out == prompt
