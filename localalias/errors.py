"""This module holds all custom exception class definitions."""


class LocalAliasError(Exception):
    """Base custom exception class."""


class AliasNotDefinedError(LocalAliasError):
    """Raised when an undefined alias is referenced in a mannor that is not allowed."""
    def __init__(self, alias):
        msg_fmt = 'Local alias "{}" is not defined in the current directory.'.format(alias)
        super().__init__(msg_fmt.format(alias))


class ArgumentError(LocalAliasError):
    """Raised when the given command-line arguments fail validation check."""
