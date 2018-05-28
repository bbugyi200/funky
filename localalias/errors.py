"""This module holds all custom exception class definitions."""


class LocalAliasError(Exception):
    """Base custom exception class."""


class AliasNotDefinedError(LocalAliasError):
    """Raised when an undefined alias is referenced in a mannor that is not allowed."""
    def __init__(self, alias=None):
        if alias is None:
            msg = 'No local aliases are defined in the current directory.'
        else:
            msg_fmt = 'Local alias "{}" is not defined in the current directory.'.format(alias)
            msg = msg_fmt.format(alias)

        super().__init__(msg)


class ArgumentError(LocalAliasError):
    """Raised when the given command-line arguments fail validation check."""
