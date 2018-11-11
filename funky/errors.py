"""This module holds all custom exception class definitions."""


class FunkyError(Exception):
    """Base custom exception class."""
    def __init__(self, *args, returncode=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.returncode = returncode


class FunkNotDefinedError(FunkyError):
    """Raised when an undefined funk is referenced in a mannor that is not allowed."""
    def __init__(self, *args, funk=None, global_=False, **kwargs):
        if funk is None:
            if global_:
                msg = 'No global funks are defined.'
            else:
                msg = 'No local funks are defined in the current directory.'
        else:
            msg_fmt = '"{}" does not match any local funks defined in the current '\
                'directory.'.format(funk)
            msg = msg_fmt.format(funk)

        super().__init__(msg, *args, **kwargs)


class ArgumentError(FunkyError):
    """Raised when the given command-line arguments fail validation check."""


class BlankDefinition(FunkyError):
    """Raised when the user attempts to define a funk using a blank definition."""
