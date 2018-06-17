"""This module holds all custom exception class definitions."""


class LocalAliasError(Exception):
    """Base custom exception class."""
    def __init__(self, *args, returncode=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.returncode = returncode


class AliasNotDefinedError(LocalAliasError):
    """Raised when an undefined alias is referenced in a mannor that is not allowed."""
    def __init__(self, *args, alias=None, global_=False, **kwargs):
        if alias is None:
            if global_:
                msg = 'No global aliases are defined.'
            else:
                msg = 'No local aliases are defined in the current directory.'
        else:
            msg_fmt = '"{}" does not match any local aliases defined in the current '\
                'directory.'.format(alias)
            msg = msg_fmt.format(alias)

        super().__init__(msg, *args, **kwargs)


class ArgumentError(LocalAliasError):
    """Raised when the given command-line arguments fail validation check."""


class BlankDefinition(LocalAliasError):
    """Raised when the user attempts to define an alias using a blank definition."""
