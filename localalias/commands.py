"""Command definitions."""

from abc import ABCMeta, abstractmethod
import json

from localalias.utils import log


class Command(metaclass=ABCMeta):
    """Base command class.

    Args:
        alias (str): local alias name.
        color (bool): if True, colorize output.
    """
    LOCALALIAS_DB_FILENAME = '.localalias.json'

    def __init__(self, alias, *, color):
        self.alias = alias
        self.color = color
        try:
            with open(self.LOCALALIAS_DB_FILENAME, 'r') as f:
                self.alias_dict = json.load(f)
        except FileNotFoundError as e:
            self.alias_dict = {}

        log.logger.debug('Existing Aliases: {}'.format(self.alias_dict))

    @abstractmethod
    def __call__(self):
        log.logger.debug('Running {} command...'.format(self.__class__.__name__))


class Add(Command):
    def __call__(self):
        super().__call__()


class Remove(Command):
    def __call__(self):
        super().__call__()


class Edit(Command):
    def __call__(self):
        super().__call__()


class Execute(Command):
    def __call__(self):
        super().__call__()


class Show(Command):
    def show_alias(self, alias):
        alias_cmd_string = self.alias_dict[alias]
        if '\n' in alias_cmd_string:
            print('{0}() {{\n\t{1}\n}}'.format(alias, alias_cmd_string.replace('\n', '\n\t')))
        else:
            print('{0}() {{ {1}; }}'.format(alias, alias_cmd_string))

    def __call__(self):
        super().__call__()
        if not self.alias_dict:
            raise RuntimeError('No local aliases are defined in the current directory.')

        if self.alias is None:
            for i, alias in enumerate(sorted(self.alias_dict)):
                self.show_alias(alias)
                if i < len(self.alias_dict) - 1:
                    print()
        else:
            self.show_alias(self.alias)
