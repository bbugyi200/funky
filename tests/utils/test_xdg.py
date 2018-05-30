"""Tests the localalias.utils.xdg utilities."""

import getpass
import os
import unittest.mock as mock

import pytest

import localalias.utils.xdg as xdg

user = getpass.getuser()


@pytest.mark.parametrize('key,expected', [
    ('config', '/home/{}/.config/localalias'.format(user)),
    ('data', '/home/{}/.local/share/localalias'.format(user)),
    ('cache', '/home/{}/.cache/localalias'.format(user))
])
def test_getdir(key, expected):
    """Tests that each user directory returned meets the XDG standard."""
    assert expected == xdg.getdir(key)


def test_getdir_failure():
    """Tests that xdg.getdir raises an exception for bad arguments."""
    with pytest.raises(ValueError):
        xdg.getdir('bad_key')
