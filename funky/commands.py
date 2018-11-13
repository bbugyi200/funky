"""Command definitions."""

from abc import ABCMeta, abstractmethod
import getpass
import json
import os
import re
import shlex
import subprocess as sp
import tempfile

from pygments import highlight
from pygments.lexers import BashLexer
from pygments.formatters import TerminalFormatter

from funky import errors
from funky import utils
from funky.utils import log


class Command(metaclass=ABCMeta):
    """Abstract base command class.

    To use a command, the corresponding command class should be used to build a command instance.
    A command instance is a callable object.

    Args:
        args (iter): The first element is necessarily a funk name. The others elements
            (if any exist) vary depending on what command is being used.
        color (bool): If True, colorize output (if command produces output).
        global_ (bool): If True, the global database will be used instead of the local database.
        verbose (bool): If True, Show command displays verbose command definition.

    IMPORTANT: The class docstring of a Command subclass is used by argparse to generate output
               for the help command.
    """
    FUNKY_DB_FILENAME = '.funky'
    GLOBALALIAS_DB_FILENAME = '/home/{}/.funky'.format(getpass.getuser())

    def __init__(self, args, *, color=False, global_=False, verbose=False):
        try:
            iter(args)
            if isinstance(args, str):
                raise ValueError
        except (TypeError, ValueError):
            args = [args]

        if global_:
            self.ACTIVE_DB_FILENAME = self.GLOBALALIAS_DB_FILENAME
        else:
            self.ACTIVE_DB_FILENAME = self.FUNKY_DB_FILENAME

        self.funk = args[0]
        self.args = args[1:]
        self.color = color
        self.verbose = verbose
        self.global_ = global_
        self.funk_dict = self.load(self.ACTIVE_DB_FILENAME)

        log.logger.vdebug('Existing Funks: {}'.format(self.funk_dict))

    def abort(self):
        """Print abort message."""
        print()
        log.logger.info('OK. Aborting...')

    def purge_db(self):
        """Removes the database file."""
        try:
            os.remove(self.ACTIVE_DB_FILENAME)
        except FileNotFoundError:
            pass

    def commit(self):
        """Saves funk changes to database."""
        if self.funk_dict:
            log.logger.debug('Committing changes to database: {}'.format(self.ACTIVE_DB_FILENAME))
            with open(self.ACTIVE_DB_FILENAME, 'w') as f:
                json.dump(self.funk_dict, f)
        else:
            log.logger.debug('Removing {}.'.format(self.ACTIVE_DB_FILENAME))
            self.purge_db()

    def load(self, DB_FILENAME):
        try:
            with open(DB_FILENAME, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    @abstractmethod
    def __call__(self):
        log.logger.debug('Running {} command.'.format(self.__class__.__name__))


class Show(Command):
    """
    When no action command is specified, the default action is to display existing funks. An
    funk name (ALIAS) can optionally be provided as an argument to display only ALIAS. If ALIAS
    ends in two periods ('..'), it is treated as a prefix instead of an exact match: all funks
    that start with ALIAS (not including the trailing '..') will be displayed.
    """
    def show(self, funk):
        """Print funk and funk command definition to stdout."""
        cmd_string = self.funk_dict[funk]
        if '\n' in cmd_string:
            show_output = '{0}() {{\n\t{1}\n}}'.format(funk, cmd_string.replace('\n', '\n\t'))
            multiline = True
        else:
            show_output = '{0}() {{ {1}; }}'.format(funk, cmd_string)
            multiline = False

        if self.verbose:
            unalias_out = 'unalias {} &> /dev/null\n'.format(funk)

            if not multiline:
                cmd_chain = re.split(' *(?:&&?|;) *', cmd_string)

                index = -1
                for i in range(len(cmd_chain)):
                    ineg = 0 - (i + 1)
                    if '$' in cmd_chain[ineg]:
                        index = ineg
                        break

                mirrored_cmd = cmd_chain[index].split(None, 1)[0]
                compdef_out = 'compdef {}={} &> /dev/null\n'.format(funk, mirrored_cmd)
            else:
                compdef_out = ''

            show_output = ''.join([unalias_out, compdef_out, show_output])

        if self.color:
            final_output = highlight(show_output, BashLexer(), TerminalFormatter()).strip()
        else:
            final_output = show_output

        print(final_output)

    def show_search(self, *, prefix):
        """Prints all funks that start with @prefix to stdout."""
        log.logger.debug('Running show command for all defined funks.')
        sorted_funks = sorted([funk for funk in self.funk_dict if funk.startswith(prefix)],
                              key=lambda x: x.lower())

        if not sorted_funks:
            raise errors.FunkNotDefinedError(funk=self.funk)

        for funk in sorted_funks:
            if self.verbose:
                print()
            self.show(funk)

    def __call__(self):
        super().__call__()
        if not self.funk_dict:
            self.purge_db()
            raise errors.FunkNotDefinedError(global_=self.global_)

        if self.funk is None:
            self.show_search(prefix='')
        elif self.funk[-2:] == '..':
            self.show_search(prefix=self.funk[:-2])
        elif self.funk not in self.funk_dict:
            raise errors.FunkNotDefinedError(funk=self.funk)
        else:
            self.show(self.funk)


class Rename(Command):
    """Rename an existing funk. OLD funk is renamed to NEW."""
    def __call__(self):
        super().__call__()
        if self.funk not in self.funk_dict:
            raise errors.FunkNotDefinedError(funk=self.funk)

        new_funk = self.args[0]
        if new_funk in self.funk_dict:
            y_or_n = utils.getch('"{}" is already in use. Overwrite? (y/n): '.format(new_funk))
            if y_or_n == 'y':
                print()
            else:
                return self.abort()

        self.funk_dict[new_funk] = self.funk_dict[self.funk]
        self.funk_dict.pop(self.funk)

        msg_fmt = 'Funk "{}" has successfully been renamed to "{}".'
        log.logger.info(msg_fmt.format(self.funk, new_funk))
        self.commit()


class Edit(Command):
    """Edit an existing funk."""
    def remove_funk(self):
        """Removes the funk defined at instance creation time."""
        self.funk_dict.pop(self.funk)
        log.logger.info('Removed funk "{}".'.format(self.funk))

    def edit_funk(self, funk=None):
        """Opens up funk definition using temp file in $EDITOR for editing.

        Args:
            funk (optional): The funk to edit. If not given, this function uses the funk defined
                at instance creation time.

        Returns (str):
            Contents of temp file after $EDITOR closes.
        """
        if funk is None:
            funk = self.funk

        tf = tempfile.NamedTemporaryFile(prefix='{}.'.format(funk),
                                         suffix='.sh',
                                         dir='/var/tmp',
                                         mode='w',
                                         delete=False)
        if funk in self.funk_dict:
            tf.write(self.funk_dict[funk])
        tf.close()

        if 'EDITOR' in os.environ:
            editor_cmd_list = shlex.split(os.environ['EDITOR'])
            log.logger.debug('Editor command set to $EDITOR: {}'.format(editor_cmd_list))
        else:
            editor_cmd_list = ['vim']
            log.logger.debug('Editor command falling back to default: {}'.format(editor_cmd_list))

        editor_cmd_list.append(tf.name)
        try:
            sp.check_call(editor_cmd_list)
        except sp.CalledProcessError:
            raise errors.FunkyError('Failed to open editor using: {}'.format(editor_cmd_list))

        tf = open(tf.name, 'r')
        edited_cmd_string = tf.read()
        tf.close()
        os.unlink(tf.name)

        if edited_cmd_string.strip() == '':
            raise errors.BlankDefinition('Funk definition cannot be blank.')

        log.logger.debug('New Command String: "%s"', edited_cmd_string)
        formatted_cmd_string = self._format_cmd_string(edited_cmd_string.strip())
        self.funk_dict[funk] = formatted_cmd_string

    def _format_cmd_string(self, cmd_string):
        """Formats command string for correct execution and display.

        It is expected that a single line funk should act the same as a normal shell funk
        would. Namely, once such a funk is defined, it is expected that the command
        `<funk> [ARGS]` would send [ARGS] to the command string that was defined for <funk>.
        Local funks behave more like shell functions tha funks, however, so this behavior
        is not automatic.

        This method solves this problem by appending $@ to a single-line command string if and
        only if the command string contains NO shell argument variables. If the user defines
        <funk> using any argument variables (e.g. $0, $1, ..., $@, $*, etc.), however, the
        command string is left unaltered.
        """
        bad_keys = [r'\$', r'\n', 'return', 'done', 'fi']
        if re.search('({})'.format('|'.join(bad_keys)), cmd_string):
            new_cmd_string = cmd_string
        else:
            new_cmd_string = '{} "$@"'.format(cmd_string)

        return new_cmd_string

    def __call__(self):
        super().__call__()
        if self.funk and self.funk not in self.funk_dict:
            raise errors.FunkNotDefinedError(funk=self.funk)

        try:
            self.edit_funk()
            log.logger.info('Edited funk "%s".', self.funk)
        except errors.BlankDefinition as e:
            log.logger.info(str(e))
            self.remove_funk()

        self.commit()


class Remove(Edit):
    """
    Remove an existing funk. Or (if ALIAS is not given) remove all funks defined in this
    directory.
    """
    def __call__(self):
        Command.__call__(self)
        if self.funk and self.funk not in self.funk_dict:
            raise errors.FunkNotDefinedError(funk=self.funk)

        if not self.funk_dict:
            raise errors.FunkNotDefinedError(global_=self.global_)

        if self.funk is None:
            log.logger.debug('Prompting to destroy local funk database.')
            prompt = 'Remove all local funks defined in this directory? (y/n): '
            y_or_n = utils.getch(prompt)
            if y_or_n == 'y':
                self.funk_dict = {}
                print()
                log.logger.info('Done. The local funk database has been removed.')
            else:
                return self.abort()
        else:
            self.remove_funk()

        self.commit()


class Add(Edit):
    """Add a new funk."""
    def __call__(self):
        Command.__call__(self)
        already_exists = False
        if self.funk in self.funk_dict:
            already_exists = True
            msg_fmt = 'Funk "{}" is already defined. Running edit command.'
            log.logger.info(msg_fmt.format(self.funk))

        try:
            self.edit_funk()
            log.logger.info('%s funk "%s".', 'Edited' if already_exists else 'Added', self.funk)
        except errors.BlankDefinition as e:
            raise errors.FunkyError(str(e))

        self.commit()
