"""Command definitions."""

from abc import ABCMeta, abstractmethod
import getpass
import json
import os
import re
import subprocess as sp
import tempfile
import time

from pygments import highlight
from pygments.lexers import BashLexer
from pygments.formatters import TerminalFormatter

from localalias import errors
from localalias import utils
from localalias.utils import log


class Command(metaclass=ABCMeta):
    """Abstract base command class.

    To use a command, the corresponding command class should be used to build a command instance.
    A command instance is a callable object.

    Args:
        args (iter): The first element is necessarily an alias name. The others elements
            (if any exist) vary depending on what command is being used.
        color (bool): If True, colorize output (if command produces output).
        global_ (bool): If True, the global database will be used instead of the local database.

    IMPORTANT: The class docstring of a Command subclass is used by argparse to generate output
               for the help command.
    """
    LOCALALIAS_DB_FILENAME = '.localalias'
    GLOBALALIAS_DB_FILENAME = '/home/{}/.globalalias'.format(getpass.getuser())

    def __init__(self, args, *, color=False, global_=False):
        try:
            iter(args)
            if isinstance(args, str):
                raise ValueError
        except (TypeError, ValueError) as e:
            args = [args]

        if global_:
            self.ACTIVE_DB_FILENAME = self.GLOBALALIAS_DB_FILENAME
        else:
            self.ACTIVE_DB_FILENAME = self.LOCALALIAS_DB_FILENAME

        self.alias = args[0]
        self.args = args[1:]
        self.color = color
        self.alias_dict = self.load(self.ACTIVE_DB_FILENAME)

        log.logger.vdebug('Existing Aliases: {}'.format(self.alias_dict))

    def purge_db(self):
        """Removes the database file."""
        try:
            os.remove(self.ACTIVE_DB_FILENAME)
        except FileNotFoundError as e:
            pass

    def commit(self):
        """Saves alias changes to database."""
        if self.alias_dict:
            log.logger.debug('Committing changes to database: {}'.format(self.ACTIVE_DB_FILENAME))
            with open(self.ACTIVE_DB_FILENAME, 'w') as f:
                json.dump(self.alias_dict, f)
        else:
            log.logger.debug('Removing {}.'.format(self.ACTIVE_DB_FILENAME))
            self.purge_db()

    def load(self, DB_FILENAME):
        try:
            with open(DB_FILENAME, 'r') as f:
                return json.load(f)
        except FileNotFoundError as e:
            return {}

    @abstractmethod
    def __call__(self):
        log.logger.debug('Running {} command.'.format(self.__class__.__name__))


class Show(Command):
    """
    When no action commands are specified, the default action is to show existing aliases. An
    alias PREFIX can optionally be given and will be used to filter the output by showing only
    those aliases that start with PREFIX.
    """
    def show(self, alias):
        """Print alias and alias command definition to stdout."""
        cmd_string = self.alias_dict[alias]
        if '\n' in cmd_string:
            show_output = '{0}() {{\n\t{1}\n}}'.format(alias, cmd_string.replace('\n', '\n\t'))
        else:
            show_output = '{0}() {{ {1}; }}'.format(alias, cmd_string)

        if self.color:
            log.logger.debug('Showing colorized output.')
            final_output = highlight(show_output, BashLexer(), TerminalFormatter()).strip()
        else:
            log.logger.debug('Showing normal output.')
            final_output = show_output

        print(final_output)

    def show_search(self, prefix=''):
        """Prints all aliases that start with @prefix to stdout."""
        log.logger.debug('Running show command for all defined aliases.')
        sorted_aliases = sorted([alias for alias in self.alias_dict if alias.startswith(prefix)])

        if not sorted_aliases:
            raise errors.AliasNotDefinedError(alias=self.alias)

        short_aliases_exist = False
        for alias in sorted_aliases:
            if '\n' not in self.alias_dict[alias]:
                self.show(alias)
                short_aliases_exist = True

        for i, alias in enumerate(sorted_aliases):
            if '\n' in self.alias_dict[alias]:
                if i > 0 or short_aliases_exist:
                    print()
                self.show(alias)

    def __call__(self):
        super().__call__()
        if not self.alias_dict:
            self.purge_db()
            raise errors.AliasNotDefinedError()

        if self.alias is None:
            self.show_search()
        else:
            self.show_search(self.alias)


class Edit(Command):
    """Edit an existing alias."""
    def remove_alias(self):
        """Removes the alias defined at instance creation time."""
        self.alias_dict.pop(self.alias)
        log.logger.info('Removed alias "{}".'.format(self.alias))

    def edit_alias(self, alias=None):
        """Opens up alias definition using temp file in $EDITOR for editing.

        Args:
            alias (optional): The alias to edit. If not given, this function uses the alias defined
                at instance creation time.

        Returns (str):
            Contents of temp file after $EDITOR closes.
        """
        if alias is None:
            alias = self.alias

        tf = tempfile.NamedTemporaryFile(prefix='{}.'.format(alias),
                                         suffix='.sh',
                                         dir=os.getcwd(),
                                         mode='w',
                                         delete=False)
        if alias in self.alias_dict:
            tf.write(self.alias_dict[alias])
        tf.close()

        if 'EDITOR' in os.environ:
            editor = os.environ['EDITOR']
            log.logger.debug('Editor set to $EDITOR: {}'.format(editor))
        else:
            editor = 'vim'
            log.logger.debug('Editor falling back to default: {}'.format(editor))

        editor_cmd_list = [editor, tf.name]
        try:
            sp.check_call(editor_cmd_list)
        except sp.CalledProcessError as e:
            raise errors.LocalAliasError('Failed to open editor using: {}'.format(editor_cmd_list))

        tf = open(tf.name, 'r')
        edited_cmd_string = tf.read()
        tf.close()
        os.unlink(tf.name)

        if edited_cmd_string.strip() == '':
            raise errors.LocalAliasError('Alias definition was left blank.')

        log.logger.debug('New Command String: "%s"', edited_cmd_string)
        formatted_cmd_string = self._format_cmd_string(edited_cmd_string.strip())
        self.alias_dict[alias] = formatted_cmd_string

    def _format_cmd_string(self, cmd_string):
        """Formats command string for correct execution and display.

        It is expected that a single line alias should act the same as a normal shell alias
        would. Namely, once such an alias is defined, it is expected that the command
        `<alias> [ARGS]` would send [ARGS] to the command string that was defined for <alias>.
        Local aliases behave more like shell functions than aliases, however, so this behavior
        is not automatic.

        This method solves this problem by appending $@ to a single-line command string if and
        only if the command string contains NO shell argument variables. If the user defines
        <alias> using any argument variables (e.g. $0, $1, ..., $@, $*, etc.), however, the
        command string is left unaltered.
        """
        if re.search(r'(\$[0-9@\*]|\n)', cmd_string):
            new_cmd_string = cmd_string
        else:
            new_cmd_string = '{} "$@"'.format(cmd_string)

        return new_cmd_string

    def __call__(self):
        super().__call__()
        if self.alias and self.alias not in self.alias_dict:
            raise errors.AliasNotDefinedError(alias=self.alias)

        try:
            self.edit_alias()
            log.logger.info('Edited alias: "%s".', self.alias)
        except errors.LocalAliasError as e:
            self.remove_alias()

        self.commit()


class Rename(Command):
    """Rename an existing alias. OLD alias is renamed to NEW."""
    def __call__(self):
        super().__call__()
        if self.alias not in self.alias_dict:
            raise errors.AliasNotDefinedError(alias=self.alias)

        new_alias = self.args[0]
        self.alias_dict[new_alias] = self.alias_dict[self.alias]
        self.alias_dict.pop(self.alias)

        msg_fmt = 'Alias "{}" has successfully been renamed to "{}".'
        log.logger.info(msg_fmt.format(self.alias, new_alias))
        self.commit()


class Remove(Edit):
    """Remove an existing alias. If no alias is given, prompt to remove all aliases (in scope)."""
    def __call__(self):
        Command.__call__(self)
        if self.alias and self.alias not in self.alias_dict:
            raise errors.AliasNotDefinedError(alias=self.alias)

        if not self.alias_dict:
            raise errors.AliasNotDefinedError()

        if self.alias is None:
            log.logger.debug('Prompting to destroy local alias database.')
            prompt = 'Remove all local aliases defined in this directory? (y/n): '
            y_or_n = utils.getch(prompt)
            if y_or_n == 'y':
                self.alias_dict = {}
                print()
                log.logger.info('Done. The local alias database has been removed.')
            else:
                print()
                log.logger.info('OK. Nothing has been done.')
                return
        else:
            self.remove_alias()

        self.commit()


class Add(Edit):
    """Add a new alias."""
    def __call__(self):
        Command.__call__(self)
        if self.alias in self.alias_dict:
            msg_fmt = 'Alias "{}" is already defined. Running edit command.'
            log.logger.info(msg_fmt.format(self.alias))
            time.sleep(1)

        try:
            self.edit_alias()
            log.logger.info('Added alias "{}".'.format(self.alias))
        except errors.LocalAliasError as e:
            raise errors.LocalAliasError('Alias definition cannot be empty.')

        self.commit()
