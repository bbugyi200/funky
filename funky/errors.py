"""This module holds all custom exception class definitions."""

from __future__ import absolute_import, division, print_function

from builtins import (  # pylint: disable=redefined-builtin,unused-import
    bytes,
    dict,
    int,
    range,
    str,
    super,
)


class FunkyError(Exception):
    """Base custom exception class."""

    def __init__(self, *args, **kwargs):
        returncode = kwargs.pop("returncode", 1)

        super().__init__(*args, **kwargs)  # type: ignore
        self.returncode = returncode


class FunkNotDefinedError(FunkyError):
    """
    Raised when an undefined funk is referenced in a mannor that is not allowed.
    """

    def __init__(self, *args, **kwargs):
        funk = kwargs.pop("funk", None)
        global_ = kwargs.pop("global_", False)

        if funk is None:
            if global_:
                msg = "No global funks are defined."
            else:
                msg = "No local funks are defined in the current directory."
        else:
            msg_fmt = (
                '"{}" does not match any local funks defined in the current '
                "directory.".format(funk)
            )
            msg = msg_fmt.format(funk)

        super().__init__(msg, *args, **kwargs)


class ArgumentError(FunkyError):
    """Raised when the given command-line arguments fail validation check."""


class BlankDefinition(FunkyError):
    """
    Raised when the user attempts to define a funk using a blank definition.
    """
