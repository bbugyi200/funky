"""Initialize and run localalias.

===== Public Interface =====
Functions: main
"""

import argparse
import enum
import sys

import localalias
from localalias import commands
from localalias.utils import log
from localalias.utils.log import logger

_LALIAS_METAVAR = 'LocalAliasName'


def main(argv=None):
    try:
        logger.debug('Starting localalias.')
        if argv is None:
            argv = sys.argv[1:]
        parser = _get_argparser()
        args = parser.parse_args(argv)
        log.init_logger(debug=args.debug)
        _validate_args(args)
        _run(args)
    except ArgumentError as e:
        logger.error('%s\n', str(e))
        parser.print_usage()
    except RuntimeError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.exception('{}: {}'.format(type(e).__name__, str(e)))
        raise


def _run(args):
    """Runs localalias.

    Decides on what commands to run based on @args.
    """
    pass


def _get_argparser():
    """Get command-line arguments.

    Returns:
        argparse.ArgumentParser object.
    """
    parser = argparse.ArgumentParser(prog='localalias', description=localalias.__doc__)
    parser.add_argument('lalias', nargs='?', default=None, metavar=_LALIAS_METAVAR,
            help='Name of the local alias/function.')
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debug mode.")
    action = parser.add_mutually_exclusive_group()
    action.add_argument('-a', Action.opt_map(Action.ADD), dest='action', action='store_const',
            const=Action.ADD,
            help='Add a new local alias/function.')
    action.add_argument('-r', Action.opt_map(Action.REMOVE), dest='action', action='store_const',
            const=Action.REMOVE,
            help='Remove an existing local alias/function.')
    action.add_argument('-e', Action.opt_map(Action.EDIT), dest='action', action='store_const',
            const=Action.EDIT,
            help='Edit local .lshrc file manually.')
    action.add_argument('-s', Action.opt_map(Action.SHOW), dest='action', action='store_const',
            const=Action.SHOW,
            help='Show an existing local alias/function. If this command is given without an '
            'argument, all local aliases/functions in scope (with respect to the current '
            'directory) are displayed.')
    action.add_argument('-x', Action.opt_map(Action.EXECUTE), dest='action', action='store_const',
            const=Action.EXECUTE, help='Execute an existing local alias/function.')
    action.set_defaults(action=Action.EXECUTE)

    return parser


class Action(enum.Enum):
    """Action Flags"""
    ADD = enum.auto()
    REMOVE = enum.auto()
    EDIT = enum.auto()
    EXECUTE = enum.auto()
    SHOW = enum.auto()

    @classmethod
    def opt_map(cls, key):
        return {cls.ADD: '--add',
                cls.REMOVE: '--remove',
                cls.EDIT: '--edit',
                cls.EXECUTE: '--execute',
                cls.SHOW: '--show'}[key]


def _validate_args(args):
    """Validates command-line arguments.

    Returns:
        @args unchanged (argparse.Namespace object), if all validation checks pass. Otherwise,
        a ValueError exception is thrown.
    """
    try:
        if args.action in [Action.ADD, Action.REMOVE, Action.EXECUTE]:
            assert args.lalias is not None
        return args
    except AssertionError as e:
        msg = 'Must also provide {} when using the {} option.'
        raise ArgumentError(msg.format(_LALIAS_METAVAR, Action.opt_map(args.action)))


class ArgumentError(ValueError):
    """Raised when the command-line arguments fail validation."""
