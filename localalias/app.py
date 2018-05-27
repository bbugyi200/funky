"""Initialize and run localalias."""

import argparse
import enum
import sys

import localalias
from localalias import commands
from localalias.utils import log

_LALIAS_METAVAR = 'LocalAliasName'


def main(argv=None):
    try:
        if argv is None:
            argv = sys.argv[1:]

        parser = _get_argparser()
        args = parser.parse_args(argv)
        log.init_logger(debug=args.debug)
        _validate_args(args)

        log.logger.debug('Starting localalias.')

        action_command = _Actions.cmd_map(args)
        action_command()
    except ValueError as e:
        log.logger.error('%s\n', str(e))
        parser.print_usage()
    except RuntimeError as e:
        log.logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        log.logger.exception('{}: {}'.format(type(e).__name__, str(e)))
        raise


def _get_argparser():
    """Get command-line arguments.

    Returns:
        argparse.ArgumentParser object.
    """
    parser = argparse.ArgumentParser(prog='localalias', description=localalias.__doc__)
    parser.add_argument('lalias', nargs='?', default=None, metavar=_LALIAS_METAVAR,
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
                 'argument, all local aliases/functions in scope (with respect to the current '
                 'directory) are displayed.')
    action.add_argument('-x', _Actions.opt_map(_Actions.EXECUTE), dest='action', action='store_const',
            const=_Actions.EXECUTE, help='Execute an existing local alias/function. This is the '
                                          'default action.')
    action.set_defaults(action=_Actions.EXECUTE)

    return parser


class _Actions(enum.Enum):
    """Action Flags"""
    ADD = enum.auto()
    REMOVE = enum.auto()
    EDIT = enum.auto()
    EXECUTE = enum.auto()
    SHOW = enum.auto()

    @classmethod
    def opt_map(cls, action):
        """Map from actions to long options."""
        return {cls.ADD: '--add',
                cls.REMOVE: '--remove',
                cls.EDIT: '--edit',
                cls.EXECUTE: '--execute',
                cls.SHOW: '--show'}[action]

    @classmethod
    def cmd_map(cls, args):
        """Map from actions to commands."""
        cmd_builder = {cls.ADD: commands.Add,
                       cls.REMOVE: commands.Remove,
                       cls.EDIT: commands.Edit,
                       cls.EXECUTE: commands.Execute,
                       cls.SHOW: commands.Show}[args.action]

        return cmd_builder(args.lalias, color=args.color)


def _validate_args(args):
    """Validates command-line arguments.

    Returns:
        @args unchanged (argparse.Namespace object), if all validation checks pass. Otherwise,
        a ValueError exception is thrown.
    """
    try:
        if args.action in [_Actions.ADD, _Actions.REMOVE, _Actions.EXECUTE]:
            assert args.lalias is not None
        return args
    except AssertionError as e:
        msg = 'You must also provide {} when using the {} option.'
        raise ValueError(msg.format(_LALIAS_METAVAR, _Actions.opt_map(args.action)))
