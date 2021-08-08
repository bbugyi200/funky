"""Tests the funky.utils.xdg utilities."""

import getpass

import pytest

from funky.utils import xdg


user = getpass.getuser()


@pytest.mark.parametrize(
    "key,expected",
    [
        ("config", "/home/{}/.config/funky".format(user)),
        ("data", "/home/{}/.local/share/funky".format(user)),
        ("cache", "/home/{}/.cache/funky".format(user)),
    ],
)
def test_getdir(key: str, expected: str) -> None:
    """Tests that each user directory returned meets the XDG standard."""
    assert expected == xdg.getdir(key)


def test_getdir_failure() -> None:
    """Tests that xdg.getdir raises an exception for bad arguments."""
    with pytest.raises(ValueError):
        xdg.getdir("bad_key")
