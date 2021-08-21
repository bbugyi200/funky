# pylint: disable=no-self-use,redefined-outer-name

"""Test --setup-shell and --init options."""

import os
from pathlib import Path
from typing import Iterator, Optional

from _pytest.capture import CaptureFixture
from pytest import fixture, mark
from syrupy.assertion import SnapshotAssertion as Snapshot

from funky import app


params = mark.parametrize

CONFIG_CONTENTS = """\
alias a='echo apple'
alias b='echo berry'
alias c='echo cherry'
"""
SHELL_TO_CONFIG = {"bash": ".bashrc", "zsh": ".zshrc"}


@fixture
def tmp_home(tmp_path: Path) -> Iterator[Path]:
    old_home = os.environ.get("HOME")
    os.environ["HOME"] = str(tmp_path)

    yield tmp_path

    if old_home:
        os.environ["HOME"] = old_home
    else:
        del os.environ["HOME"]


@params("shell", ["bash", "zsh"])
def test_init(shell: str, snapshot: Snapshot, capsys: CaptureFixture) -> None:
    exit_code = app.main(["--init", shell])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert captured.out == snapshot


@params(
    "shell,contents",
    [
        ("bash", None),
        ("bash", CONFIG_CONTENTS),
        ("zsh", None),
        ("zsh", CONFIG_CONTENTS),
    ],
)
def test_setup_shell(
    shell: str, contents: Optional[str], tmp_home: Path, snapshot: Snapshot
) -> None:
    config_file = tmp_home / SHELL_TO_CONFIG[shell]
    if contents:
        config_file.write_text(contents)

    exit_code = app.main(["--setup-shell", shell])
    assert exit_code == 0

    assert config_file.read_text() == snapshot
