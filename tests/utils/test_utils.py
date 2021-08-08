"""Tests miscellaneous utilities."""

from unittest import mock

from _pytest.capture import CaptureFixture

from funky import utils


@mock.patch("funky.utils.tty")
@mock.patch("funky.utils.termios")
@mock.patch("funky.utils.sys.stdin.fileno")
@mock.patch("funky.utils.sys.stdin.read")
def test_getch(
    read: mock.MagicMock,
    fileno: mock.MagicMock,
    _: mock.MagicMock,
    __: mock.MagicMock,
    capsys: CaptureFixture,
) -> None:
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
