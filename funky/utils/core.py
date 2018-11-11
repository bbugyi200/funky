"""Core utilities.

The contents of this module are intended to be imported directly into the utils
package's global namespace. Any classes/functions defined in this module MUST
be included in __all__ or they will NOT be accessible from the utils package.
"""

import sys
import tty
import termios

__all__ = ['getch']


def getch(prompt=None):
    """Reads a single character from stdin.

    Args:
        prompt (optional): prompt that is presented to user.

    Returns:
        The single character that was read.
    """
    if prompt:
        sys.stdout.write(prompt)

    sys.stdout.flush()

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
