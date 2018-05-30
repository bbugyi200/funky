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

_ALIAS_METAVAR = 'LocalAliasName'


def main(argv=None):
    try:
        if argv is None:
            argv = sys.argv[1:]

        parser = _get_argparser()
        args = parser.parse_args(argv)

        log.init_logger(debug=args.debug)
        if args.action == _Actions.EXECUTE and not args.debug:
            log.silence_streams()

        log.logger.debug('Starting localalias.')
        log.logger.vdebug('Command-line Arguments: {}'.format(args))

        _validate_args(args)

        action_command = _Actions.cmd_map(args)
        action_command()
    except errors.ArgumentError as e:
        log.logger.error('%s\n', str(e))
        parser.print_usage()
        return 1
    except errors.LocalAliasError as e:
        log.logger.error(str(e))
        return 1
    except Exception as e:
        log.logger.exception('{}: {}'.format(type(e).__name__, str(e)))
        raise


def _get_argparser():
    """Get command-line arguments.

    Returns:
        argparse.ArgumentParser object.
    """
    parser = argparse.ArgumentParser(prog='localalias', description=localalias.__doc__)
    parser.add_argument('alias', nargs='?', default=None, metavar=_ALIAS_METAVAR,
            help='Name of the local alias/function.')
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debug mode.")
    parser.add_argument('-c', '--color', action='store_true', help="Colorize output.")

    action = parser.add_mutually_exclusive_group()
    action.add_argument('-a', _Actions.opt_map(_Actions.ADD), dest='action', action='store_const',
            const=_Actions.ADD,
            help='Add a new local alias/function.')
    action.add_argument('-r', _Actions.opt_map(_Actions.REMOVE), dest='action', action='store_const',
            const=_Actions.REMOVE,
            help='Remove an existing local alias/function.')
    action.add_argument('-e', _Actions.opt_map(_Actions.EDIT), dest='action', action='store_const',
            const=_Actions.EDIT,
            help='Edit an existing local alias/function. If this command is given without '
                 'an argument, the local .lshrc file will be opened using your default editor.')
    action.add_argument('-s', _Actions.opt_map(_Actions.SHOW), dest='action', action='store_const',
            const=_Actions.SHOW,
            help='Show an existing local alias/function. If this command is given without an '
                 'argument, all local aliases/functions in scope are displayed. (default action)')
    action.add_argument('-x', _Actions.opt_map(_Actions.EXECUTE), dest='action', action='store_const',
            const=_Actions.EXECUTE, help='Execute an existing local alias/function.')
    action.set_defaults(action=_Actions.SHOW)

    parser.add_argument('cmd_args', nargs=argparse.REMAINDER,
            help='Captures variable number of command-line arguments meant for local alias. These '
                 'arguments are only applicable when used with the {} '
                 'option.'.format(_Actions.opt_map(_Actions.EXECUTE)))

    return parser


class _Actions(enum.Enum):
    """Action Flags"""
    ADD = 1
    REMOVE = 2
    EDIT = 3
    EXECUTE = 4
    SHOW = 5

    @classmethod
    def opt_map(cls, action):
        """Map from actions to long options.

        Long options are used in error messages. This function prevents unnecessary duplication.
        """
        return {cls.ADD: '--add',
                cls.REMOVE: '--remove',
                cls.EDIT: '--edit',
                cls.EXECUTE: '--execute',
                cls.SHOW: '--show'}[action]

    @classmethod
    def cmd_map(cls, args):
        """Map from actions to commands.

        This function is intended to serve as this module's interface to the commands API.
        """
        cmd_builder = {cls.ADD: commands.Add,
                       cls.REMOVE: commands.Remove,
                       cls.EDIT: commands.Edit,
                       cls.EXECUTE: commands.Execute,
                       cls.SHOW: commands.Show}[args.action]

        return cmd_builder(args.alias, cmd_args=args.cmd_args, color=args.color)


def _validate_args(args):
    """Validates command-line arguments.

    Returns:
        @args unchanged (argparse.Namespace object), if all validation checks pass. Otherwise,
        a ValueError exception is thrown.
    """
    try:
        if args.action in [_Actions.ADD, _Actions.EXECUTE]:
            assert args.alias is not None
        return args
    except AssertionError as e:
        msg_fmt = 'You must also provide a {} when using the {} option.'
        raise errors.ArgumentError(msg_fmt.format(_ALIAS_METAVAR, _Actions.opt_map(args.action)))
