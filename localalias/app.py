"""Initialize and run localalias.

Do not execute this file directly. Use __main__.py by executing this modules containing directory.
In other words, use `python localalias`.
"""

import argparse
import enum
import sys

import localalias
from localalias import commands
from localalias import errors
from localalias.utils import log


def main(argv=None):
    try:
        if argv is None:
            argv = sys.argv[1:]

        parser = _get_argparser()
        args = parser.parse_args(argv)

        log.init_logger(debug=args.debug)

        _validate_args(args, _CmdAction.flag)

        log.logger.debug('Starting localalias.')
        log.logger.vdebug('Command-line Arguments: {}'.format(args))

        _CmdAction.command(args)
    except errors.ArgumentError as e:
        log.logger.error('%s\n', str(e))
        parser.print_usage()
        return 2
    except errors.LocalAliasError as e:
        log.logger.debug('Exit Status: %s', e.returncode)
        log.logger.error(str(e))
        return e.returncode
    except Exception as e:
        log.logger.exception('{}: {}'.format(type(e).__name__, str(e)))
        raise


def _get_argparser():
    """Get command-line arguments.

    Returns:
        argparse.ArgumentParser object.
    """
    parser = argparse.ArgumentParser(prog='localalias', description=localalias.__doc__)
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debug mode.")
    parser.add_argument('--version', action='version',
            version='%(prog)s {}'.format(localalias.__version__))
    parser.add_argument('-c', '--color', action='store_true', help="Colorize output.")
    parser.add_argument('-g', '--global', dest='global_', action='store_true',
                        help='Run action command with global scope.')

    command_group = parser.add_argument_group(
        title='Action Commands',
        description='All of these options act on the current set of local aliases in some way. If '
                    'no action command is provided, the default action is to show all of the '
                    'local aliases currently in scope. These commands are mutually exclusive.'
    )
    command_group.add_argument(_CmdFlag.ADD.value, nargs=1, dest='command_args', action=_CmdAction,
                               metavar='ALIAS', help=commands.Add.__doc__)
    command_group.add_argument(_CmdFlag.REMOVE.value, nargs='?', dest='command_args',
                               action=_CmdAction, metavar='ALIAS', help=commands.Remove.__doc__)
    command_group.add_argument(_CmdFlag.EDIT.value, nargs=1, dest='command_args',
                               action=_CmdAction, metavar='ALIAS', help=commands.Edit.__doc__)
    command_group.add_argument(_CmdFlag.EXECUTE.value, nargs=argparse.REMAINDER,
                               dest='command_args', action=_CmdAction, metavar='ARG',
                               help=argparse.SUPPRESS)
    command_group.add_argument(_CmdFlag.RENAME.value, nargs=2, dest='command_args',
                               action=_CmdAction, metavar=('OLD', 'NEW'),
                               help=commands.Rename.__doc__)
    command_group.add_argument('command_args', nargs='?', action=_CmdAction, metavar='PREFIX',
                               help=commands.Show.__doc__)

    return parser


def _validate_args(args, flag):
    """Run extra validation checks on command-line arguments.

    This function also makes necessary changes to the environment when necessary given certain
    argument combinations (e.g. silence logs when -x is present but -d is not).
    """
    if flag == _CmdFlag.EXECUTE and args.global_:
        raise errors.ArgumentError(
            'The --global option is redundant when used with -x. Both local and global aliases '
            'are always checked (in that order) when the -x option is given.'
        )

    if flag == _CmdFlag.EXECUTE and len(args.command_args) < 1:
        raise errors.ArgumentError(
            'The -x option requires atleast one argument. Namely, the alias that you would like '
            'to execute.'
        )

    if flag == _CmdFlag.EXECUTE and not args.debug:
        log.silence_streams()


class _CmdAction(argparse.Action):
    """Custom ArgumentParser Action for Action Commands"""
    flag = None
    option_string = None

    def __call__(self, parser, namespace, values, option_string):
        if self.__class__.flag is None:
            self.__class__.flag = _CmdFlag(option_string)
            self.__class__.option_string = option_string
        elif option_string is not None:
            raise errors.ArgumentError(
                'Option {} can not be used with option {}. All action commands are mutually '
                'exclusive.'.format(option_string, self.__class__.option_string)
            )
        else:
            return

        try:
            iter(values)
            if isinstance(values, str):
                raise ValueError
        except (TypeError, ValueError) as e:
            values = [values]

        setattr(namespace, self.dest, values)

    @classmethod
    def command(cls, args):
        """Map from actions to commands."""
        cmd_builder = {_CmdFlag.ADD: commands.Add,
                       _CmdFlag.REMOVE: commands.Remove,
                       _CmdFlag.EDIT: commands.Edit,
                       _CmdFlag.EXECUTE: commands.Execute,
                       _CmdFlag.RENAME: commands.Rename,
                       _CmdFlag.SHOW: commands.Show}[cls.flag]

        cmd = cmd_builder(args.command_args, color=args.color, global_=args.global_)
        return cmd()


class _CmdFlag(enum.Enum):
    """Command Flags

    The value of each command flag will be used by argparse to generate the option string
    corresponding to that command.
    """
    ADD = '-a'
    REMOVE = '-r'
    EDIT = '-e'
    EXECUTE = '-x'
    SHOW = None
    RENAME = '-R'
