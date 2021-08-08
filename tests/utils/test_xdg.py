"""Tests the funky.utils.xdg utilities."""

import getpass

import pytest

import funky.utils.xdg as xdg


user = getpass.getuser()


@pytest.mark.parametrize(
    "key,expected",
    [
        ("config", "/home/{}/.config/funky".format(user)),
        ("data", "/home/{}/.local/share/funky".format(user)),
        ("cache", "/home/{}/.cache/funky".format(user)),
    ],
)
def test_getdir(key, expected):
    """Tests that each user directory returned meets the XDG standard."""
    assert expected == xdg.getdir(key)


def test_getdir_failure():
    """Tests that xdg.getdir raises an exception for bad arguments."""
    with pytest.raises(ValueError):
        xdg.getdir("bad_key")
