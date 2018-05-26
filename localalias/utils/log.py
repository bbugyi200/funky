"""Loggers and utilities related to logging."""

import logging

import localalias.utils.xdg as xdg

logger = logging.getLogger("localalias")


def init_logger(logger, *, debug=False):
    """Initializes the main logger.

    Args:
        logger: logging.Logger object.
        debug: True if debugging is enabled.
    """
    logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    formatter = _getFormatter()
    sh.setFormatter(formatter)
    sh.setLevel(logging.DEBUG if debug else logging.INFO)
    logger.addHandler(sh)

    if debug:
        logfile_path = '{}/debug.log'.format(xdg.getdir('data'))
        fh = logging.FileHandler(logfile_path)
        formatter = _getFormatter(verbose=True)
        fh.setFormatter(formatter)
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)


def _getFormatter(*, verbose=False):
    """ Get log formatter.

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
