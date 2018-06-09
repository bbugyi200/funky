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
        if _CmdAction.flag == _CmdFlag.EXECUTE and not args.debug:
            log.silence_streams()

        log.logger.debug('Starting localalias.')
        log.logger.vdebug('Command-line Arguments: {}'.format(args))

        _CmdAction.command(args)
    except errors.ArgumentError as e:
        log.logger.error('%s\n', str(e))
        parser.print_usage()
        return 1
    except errors.LocalAliasError as e:
        log.logger.error('%s (exit status: %s)', str(e), e.returncode)
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

    command_group = parser.add_argument_group(
        title='Action Commands',
        description='All of these options act on the current set of local aliases in some way. If '
                    'no action command is provided, the default action is to show all of the '
                    'local aliases currently in scope. These commands are mutually exclusive.'
    )
    command_group.add_argument(
        '-a', nargs=1, dest='command_args', action=_CmdAction, metavar='ALIAS',
        help='Add a new local alias.'
    )
    command_group.add_argument(
        '-r', nargs='?', dest='command_args', action=_CmdAction, metavar='ALIAS',
        help='Remove an existing local alias. If no alias is given, prompt to remove all local '
             'aliases (in scope).'
    )
    command_group.add_argument(
        '-e', nargs=1, dest='command_args', action=_CmdAction,
        metavar='ALIAS',
        help='Edit an existing local alias.'
    )
    command_group.add_argument(
        '-x', nargs='+', dest='command_args', action=_CmdAction, metavar='ARG',
        help='Execute an existing local alias. The first argument must be the alias to execute. '
             'The remaining arguments are optional. If given, they are passed on to the command '
             'that is to be executed. This is typically not done manually.'
    )
    command_group.add_argument(
        '-R', nargs=2, dest='command_args', action=_CmdAction, metavar=('OLD', 'NEW'),
        help='Rename an existing local alias. OLD is renamed to NEW.'
    )
    command_group.add_argument(
        'command_args', nargs='?', action=_CmdAction, metavar='PREFIX',
        help='When no action commands are specified, the default action is to show existing '
             'aliases. An alias PREFIX can optionally be given and will be used to filter the '
             'output by showing only those aliases that start with PREFIX.'
    )

    return parser


class _CmdAction(argparse.Action):
    """Custom ArgumentParser Action for Action Commands"""
    flag = None
    option_string = None

    def __call__(self, parser, namespace, values, option_string):
        if self.__class__.flag is None:
            self.__class__.flag = self._flag_map(option_string)
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

        cmd = cmd_builder(args.command_args, color=args.color)
        return cmd()

    def _flag_map(self, option_string):
        """Maps option strings to Command Flags"""
        return {'-a': _CmdFlag.ADD,
                '-r': _CmdFlag.REMOVE,
                '-e': _CmdFlag.EDIT,
                '-x': _CmdFlag.EXECUTE,
                '-R': _CmdFlag.RENAME,
                None: _CmdFlag.SHOW}[option_string]


class _CmdFlag(enum.Enum):
    """Command Flags"""
    ADD = 1
    REMOVE = 2
    EDIT = 3
    EXECUTE = 4
    SHOW = 5
    RENAME = 6
