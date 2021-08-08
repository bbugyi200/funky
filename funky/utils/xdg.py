"""XDG Utilities"""

import errno
import getpass
import os
from typing import Callable


_user = getpass.getuser()


def getdir(userdir: str) -> str:
    """Get XDG User Directory.

    Args:
        userdir (str): one of the four defined XDG user directories ('config',
                       'data', 'runtime', or 'cache').

    Returns:
        Full user directory path, as specified by the XDG standard.
    """
    userdir = userdir.lower()
    userdir_opts = {"config", "data", "runtime", "cache"}
    if userdir not in userdir_opts:
        raise ValueError(
            "Argument @userdir MUST be one of the following "
            "options: {}".format(userdir_opts)
        )

    getters = {
        "config": _getter_factory("XDG_CONFIG_HOME", "{}/.config/funky"),
        "data": _getter_factory("XDG_DATA_HOME", "{}/.local/share/funky"),
        "runtime": _getter_factory("XDG_RUNTIME_DIR", "/run/user/1000/funky"),
        "cache": _getter_factory("XDG_CACHE_HOME", "{}/.cache/funky"),
    }

    return getters[userdir]()


def _getter_factory(envvar: str, dirfmt: str) -> Callable[[], str]:
    """
    Returns XDG getter function that serves to fetch some XDG standard
    directory.

    Args:
        envvar (str): one of the four defined XDG environment variables that
                      correspond to the XDG user directories.
        dirfmt: format string used to model the default path for the given XDG
                       user directory.

    Returns:
        Function that retrieves the full path for the desired XDG user
        directory.
    """

    def _getter() -> str:
        if envvar in os.environ:
            xdg_dir = "{}/funky".format(os.environ[envvar])
        else:
            if dirfmt.count("{}") > 0:
                xdg_dir = dirfmt.format(os.path.expanduser("~"))
            else:
                xdg_dir = dirfmt

        _create_dir(xdg_dir)
        return xdg_dir

    return _getter


def _create_dir(directory: str) -> None:
    """Create directory if it does not already exist.

    Args:
        directory: full directory path.
    """
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
