"""Loggers and utilities related to logging.

Attributes:
    logger: main logging.Logger object.
"""

import logging

import localalias.utils.xdg as xdg

logger = logging.getLogger("localalias")

# This assignment is temporary. Will be removed when I define a VDEBUG logging level.
logger.vdebug = logger.debug


def init_logger(*, debug=False):
    """Initializes the main logger."""
    root = logging.getLogger()
    level = logging.DEBUG if debug else logging.INFO
    root.setLevel(level)

    sh = logging.StreamHandler()
    formatter = _getFormatter()
    sh.setFormatter(formatter)
    sh.setLevel(level)
    root.addHandler(sh)

    if debug:
        logfile_path = '{}/debug.log'.format(xdg.getdir('data'))
        fh = logging.FileHandler(logfile_path)
        formatter = _getFormatter(verbose=True)
        fh.setFormatter(formatter)
        fh.setLevel(level)
        root.addHandler(fh)
        root.debug('Debug mode enabled.')


def silence_streams():
    """Silence stream log handlers."""
    root = logging.getLogger()
    for handler in root.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setLevel(logging.CRITICAL)


def _getFormatter(*, verbose=False):
    """Get log formatter.

    Args:
        verbose: True if a more verbose log format is desired.

    Returns:
        logging.Formatter object.
    """
    base_formatting = '[%(levelname)s] %(message)s'

    if verbose:
        formatter = logging.Formatter('[%(process)s] (%(asctime)s) {}'.format(base_formatting),
                                      datefmt='%Y-%m-%d %H:%M:%S')
    else:
        formatter = logging.Formatter(base_formatting)

    return formatter
