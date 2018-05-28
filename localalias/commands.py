"""Command definitions."""

from abc import ABCMeta, abstractmethod
import json
import os
import subprocess as sp
import tempfile

from localalias.utils import log


class Command(metaclass=ABCMeta):
    """Base command class.

    Args:
        alias (str): local alias name.
        color (bool): if True, colorize output.
    """
    LOCALALIAS_DB_FILENAME = '.localalias.json'

    def __init__(self, alias, *, color=False):
        self.alias = alias
        self.color = color
        try:
            with open(self.LOCALALIAS_DB_FILENAME, 'r') as f:
                self.alias_dict = json.load(f)
        except FileNotFoundError as e:
            self.alias_dict = {}

        log.logger.debug('Existing Aliases: {}'.format(self.alias_dict))

    def commit(self):
        """Saves alias changes to local database."""
        with open(self.LOCALALIAS_DB_FILENAME, 'w') as f:
            json.dump(self.alias_dict, f)

    @abstractmethod
    def __call__(self):
        log.logger.debug('Running {} command...'.format(self.__class__.__name__))


class Execute(Command):
    def __call__(self):
        super().__call__()


class Show(Command):
    def show(self, alias):
        """Print alias and alias command definition to stdout."""
        alias_cmd_string = self.alias_dict[alias]
        if '\n' in alias_cmd_string:
            print('{0}() {{\n\t{1}\n}}'.format(alias, alias_cmd_string.replace('\n', '\n\t')))
        else:
            print('{0}() {{ {1}; }}'.format(alias, alias_cmd_string))

    def show_all(self):
        """Prints all defined alias definitions to stdout."""
        for i, alias in enumerate(sorted(self.alias_dict)):
            self.show(alias)
            if i < len(self.alias_dict) - 1:
                print()

    def __call__(self):
        super().__call__()
        if not self.alias_dict:
            raise RuntimeError('No local aliases are defined in the current directory.')

        if self.alias and self.alias not in self.alias_dict:
            raise _AliasNotDefinedError(self.alias)

        if self.alias is None:
            self.show_all()
        else:
            self.show(self.alias)


class Edit(Command):
    def edit_alias(self):
        """Opens up alias definition using temp file in $EDITOR for editing.

        Uses alias defined at instance creation time.

        Returns (str):
            Contents of temp file after $EDITOR closes.
        """
        tf = tempfile.NamedTemporaryFile(suffix='.tmp', mode='w', delete=False)
        if self.alias in self.alias_dict:
            tf.write(self.alias_dict[self.alias])
        tf.close()

        if 'EDITOR' in os.environ:
            editor = os.environ['EDITOR']
        else:
            editor = 'vim'

        sp.check_call([editor, tf.name])

        tf = open(tf.name, 'r')
        edited_alias_cmd_string = tf.read()
        tf.close()
        os.unlink(tf.name)

        return edited_alias_cmd_string.strip()

    def __call__(self):
        super().__call__()
        if self.alias not in self.alias_dict:
            raise _AliasNotDefinedError(self.alias)
        self.alias_dict[self.alias] = self.edit_alias()
        self.commit()


class Remove(Show):
    def __call__(self):
        Command.__call__(self)
        if self.alias not in self.alias_dict:
            raise _AliasNotDefinedError(self.alias)
        self.alias_dict.pop(self.alias)
        self.commit()

        if self.alias_dict:
            self.show_all()
        else:
            os.remove(self.LOCALALIAS_DB_FILENAME)


class Add(Edit):
    def __call__(self):
        Command.__call__(self)
        self.alias_dict[self.alias] = self.edit_alias()
        self.commit()


class _AliasNotDefinedError(RuntimeError):
    """Raised when an undefined alias is referenced in a mannor that is not allowed."""
    def __init__(self, alias):
        msg_fmt = 'Local alias "{}" is not defined in the current directory.'.format(alias)
        super().__init__(msg_fmt.format(alias))
