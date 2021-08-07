from collections import namedtuple
import os
from pathlib import Path

from scripts import post_install


def test_copy_sh_ext__ENVVAR_DEFINED(xdg_data_home: Path) -> None:
    Install = namedtuple("Install", ["root"])
    install = Install(None)
    post_install._copy_sh_ext(install)  # pylint: disable=protected-access

    assert os.path.exists(f"{xdg_data_home}/funky/funky.sh")


def test_copy_sh_ext__ENVVAR_NOT_DEFINED():
    old_data_dir = os.environ.get("XDG_DATA_HOME", None)

    if "XDG_DATA_HOME" in os.environ:
        del os.environ["XDG_DATA_HOME"]

    delete_user = False
    if "USER" not in os.environ:
        delete_user = True
        os.environ["USER"] = "bryan"

    Install = namedtuple("Install", ["root"])
    install = Install("/tmp/")
    post_install._copy_sh_ext(install)  # pylint: disable=protected-access

    os.path.exists(
        f"/tmp/home/{os.environ['USER']}/.local/share/funky/funky.sh"
    )
    os.system("rm -rf /tmp/home")

    if old_data_dir:
        os.environ["XDG_DATA_HOME"] = old_data_dir

    if delete_user:
        del os.environ["USER"]
