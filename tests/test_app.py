"""Tests for main application (entry point)."""

import functools
from typing import List
from unittest import mock

import pytest

import funky
from funky import app, errors


@pytest.mark.parametrize(
    "argv,cmd_cls_string",
    [
        (["-a", "new_funk"], "Add"),
        (["-e", "new_funk"], "Edit"),
        (["-r", "new_funk"], "Remove"),
    ],
)
@mock.patch("funky.app.commands")
def test_main(
    commands: mock.MagicMock, argv: List[str], cmd_cls_string: str
) -> None:
    """Tests that arguments are parsed correctly."""
    setattr(commands, cmd_cls_string, mock.Mock())
    cmd_class = getattr(commands, cmd_cls_string)
    app.main(argv)

    cmd_class.assert_called_once_with(
        argv[1:], color=False, global_=False, verbose=False
    )
    app._CmdAction.flag = None  # pylint: disable=protected-access


@pytest.mark.parametrize("argv", [["-a", "new_funk", "-e", "existing_funk"]])
@mock.patch("funky.utils.log.logger")
def test_main_validate_args(logger: mock.MagicMock, argv: List[str]) -> None:
    """Tests that arguments are validated properly."""
    assert app.main(argv) == 2
    logger.error.called_once()
    funky.app._CmdAction.flag = None  # pylint: disable=protected-access
    funky.app._CmdAction.option_string = (
        None  # pylint: disable=protected-access
    )


@mock.patch("funky.app._get_argparser")
def test_main_exceptions(_get_argparser: mock.MagicMock) -> None:
    """Tests that main handles exceptions appropriately."""

    class TestError(Exception):
        pass

    def raise_error(opt: int, verbose: bool = True) -> None:
        del verbose

        if opt == 1:
            raise errors.FunkyError(returncode=5)

        if opt == 2:
            raise TestError("Test Exception")

    _get_argparser.side_effect = functools.partial(raise_error, 1)
    assert app.main() == 5

    _get_argparser.side_effect = functools.partial(raise_error, 2)
    with pytest.raises(TestError):
        app.main()
