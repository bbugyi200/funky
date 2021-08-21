"""Test --setup-shell and --init options."""

from _pytest.capture import CaptureFixture
from pytest import mark
from syrupy.assertion import SnapshotAssertion as Snapshot

from funky import app


params = mark.parametrize


@params("shell", ["bash", "zsh"])
def test_init(shell: str, snapshot: Snapshot, capsys: CaptureFixture) -> None:
    app.main(["--init", shell])
    captured = capsys.readouterr()
    assert captured.out == snapshot
