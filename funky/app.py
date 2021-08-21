"""Initialize and run funky.

Do not execute this file directly. Use __main__.py by executing this modules
containing directory.  In other words, use `python funky`.
"""

import argparse
from importlib.resources import read_text
from pathlib import Path
import sys
from typing import List, Optional, Sequence, Union

import funky
from funky import commands, errors
from funky.utils import log


_SUPPORTED_SHELLS = ["bash", "zsh"]


def main(argv: Sequence[str] = None) -> int:
    try:
        if argv is None:
            argv = sys.argv[1:]

        verbose = any(x in argv for x in ["--verbose", "-v", "-hv", "-vh"])
        parser = _get_argparser(verbose=verbose)
        args = parser.parse_args(argv)

        log.init_logger(debug=args.debug, verbose=args.verbose)
        log.logger.debug("Starting funky.")
        log.logger.vdebug("argv = {}".format(argv))  # type: ignore
        log.logger.vdebug("Command-line Arguments: {}".format(args))  # type: ignore

        if args.init:
            return run_init(args.init)

        if args.setup_shell:
            return run_setup_shell(args.setup_shell)

        _CmdAction.command(args)
    except errors.ArgumentError as e:
        log.logger.error("%s\n", str(e))
        parser.print_usage()
        return 2
    except errors.FunkyError as e:
        log.logger.debug("Exit Status: %s", e.returncode)
        log.logger.error(str(e))
        return e.returncode
    except Exception as e:
        log.logger.exception("%s: %s", type(e).__name__, str(e))
        raise

    return 0


def run_init(shell: str) -> int:
    del shell  # all supported shells use the same code ATM

    funky_sh = read_text("scripts.shell", "funky.sh")
    print(funky_sh, end="")
    return 0


def run_setup_shell(shell: str) -> int:
    if shell == "zsh":
        config_base = ".zshrc"
    else:
        assert shell == "bash"
        config_base = ".bashrc"

    config_path = Path.home() / config_base
    funky_init = f"funky --init {shell}"
    if not config_path.exists() or funky_init not in config_path.read_text():
        with config_path.open("a") as f:
            cmd = (
                "\n# setup funky\n"
                "command -v funky &>/dev/null &&"
                f' eval "$({funky_init})"'
            )
            log.logger.info(
                "Appending %d lines to your %s file...",
                len(cmd.split("\n")),
                config_base,
            )
            f.write(cmd)
    return 0


def _get_argparser(verbose: bool = False) -> argparse.ArgumentParser:
    """Get command-line arguments.

    Args:
        verbose (bool): If True, do not suppress the help output of any
                        arguments.

    Returns:
        argparse.ArgumentParser object.
    """
    parser = argparse.ArgumentParser(prog="funky", description=funky.__doc__)

    init_group = parser.add_mutually_exclusive_group()
    init_group.add_argument(
        "--setup-shell",
        choices=_SUPPORTED_SHELLS,
        help="Ensure your shell is configured correctly.",
    )
    init_group.add_argument(
        "--init",
        choices=_SUPPORTED_SHELLS,
        help=(
            "Initialize your shell environments. This should be run from your"
            " .bashrc / .zshrc file."
        ),
    )

    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug mode."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output."
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {}".format(funky.__version__),
    )
    parser.add_argument(
        "--color",
        nargs=1,
        choices=("y", "n"),
        default="n",
        help="Colorize funk definitions.",
    )

    parser.add_argument(
        "-g",
        "--global",
        dest="global_",
        action="store_true",
        help=("Enable global scope." if verbose else argparse.SUPPRESS),
    )

    def format_docstring(doc: Optional[str]) -> str:
        """Converts command docstring to argparse help doc"""
        if doc is None:
            doc = ""
        return doc.strip().replace("\n", " ")

    command_group = parser.add_argument_group(
        title="Action Commands",
        description=(
            "All of these options act on the current set of local funks in "
            "some way. If no action command is provided, the default action "
            "is to display all of the local funks currently in scope. These "
            "commands are mutually exclusive."
        ),
    )
    command_group.add_argument(
        _CmdFlag.ADD,
        nargs=1,
        dest="command_args",
        action=_CmdAction,
        metavar="FUNK",
        help=format_docstring(commands.Add.__doc__),
    )
    command_group.add_argument(
        _CmdFlag.REMOVE,
        nargs="?",
        dest="command_args",
        action=_CmdAction,
        metavar="FUNK",
        help=format_docstring(commands.Remove.__doc__),
    )
    command_group.add_argument(
        _CmdFlag.EDIT,
        nargs=1,
        dest="command_args",
        action=_CmdAction,
        metavar="FUNK",
        help=format_docstring(commands.Edit.__doc__),
    )
    command_group.add_argument(
        _CmdFlag.RENAME,
        nargs=2,
        dest="command_args",
        action=_CmdAction,
        metavar=("OLD", "NEW"),
        help=format_docstring(commands.Rename.__doc__),
    )
    command_group.add_argument(
        "command_args",
        nargs="?",
        action=_CmdAction,
        metavar="FUNK",
        help=format_docstring(commands.Show.__doc__),
    )

    return parser


class _CmdAction(argparse.Action):
    """Custom ArgumentParser Action for Action Commands"""

    flag: Optional[str] = None
    option_string = None

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[None, str, Sequence[str]],
        option_string: str = None,
    ) -> None:
        if self.__class__.flag is None:
            self.__class__.flag = option_string
            self.__class__.option_string = option_string
        elif option_string is not None:
            raise errors.ArgumentError(
                "Option {} can not be used with option {}. All action "
                "commands are mutually exclusive.".format(
                    option_string, self.__class__.option_string
                )
            )
        else:
            return

        dest: List[Optional[str]]
        if values is None or isinstance(values, str):
            dest = [values]
        else:
            dest = list(values)

        setattr(namespace, self.dest, dest)

    @classmethod
    def command(cls, args: argparse.Namespace) -> None:
        """Map from actions to commands."""
        cmd_builder = {
            _CmdFlag.ADD: commands.Add,
            _CmdFlag.REMOVE: commands.Remove,
            _CmdFlag.EDIT: commands.Edit,
            _CmdFlag.RENAME: commands.Rename,
            _CmdFlag.SHOW: commands.Show,
        }[cls.flag]

        cmd = cmd_builder(  # type: ignore[abstract]
            args.command_args,
            color=(args.color[0] == "y"),
            global_=args.global_,
            verbose=args.verbose,
        )
        return cmd()


class _CmdFlag:
    """Command Flags

    The value of each command flag will be used by argparse to generate the
    option string corresponding to that command.
    """

    ADD = "-a"
    REMOVE = "-r"
    EDIT = "-e"
    SHOW = None
    RENAME = "-R"
