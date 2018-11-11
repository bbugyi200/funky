# Change Log

All notable changes to this project will be documented in this file. This project adheres to
[Semantic Versioning](https://semver.org/), though minor breaking changes can happen in minor
releases.

### v3.0.1 (2018-11-11)

Fixed:

* PyPI markdown rendering

### v3.0.0 (2018-11-10)

Changed:

* Renamed project from 'localalias' to 'funky'.

### v2.6.1 (2018-10-20)

Fixed:

* Editor call breaks when $EDITOR includes command-line options

### v2.6.0 (2018-09-11)

Added:

* Automatically add zsh autocompletion for single-line funks.

Changed:

* The show command (used by default when no other command group is specified) now only treats
  the given funk as a prefix if it ends in two periods (``..``). Otherwise, the funk is matched exactly. Prior
  to this change, there was no way to specify an exact match.

Fixed:

* funky.zsh incorrectly assumes that $HOME==/home/<user>
* If the Rename command (``-R``) is used to rename a funk to an existing funk's name, the user
  should be prompted to confirm.
* Using ``-vh`` or ``-hv`` command-line options should show verbose help output.
* Moved 'timestamp' and 'localpath' files to user specific directory to keep this data from being
  overwritten by other users (notably, to keep root from overwritting these files).

Removed:

* Oh-My-ZSH plugin support. The ``funky.zsh`` script will now need to be manually sourced
  into the user's ``zshrc``.

### v2.5.1 (2018-06-17)

Fixed:

* When traveling back to the project root directory (the first directory to have sourced local
  functions), it is certain that sourcing the global functions will not override any local
  functions defined in parent directories. Since it is safe, it is preferred to do so; otherwise,
  some global functions may still be overriden by local ones even after traveling back to an
  ancestor of the directory where said local functions were defined. This can still happen, but
  sourcing global functions when traveling back to the project root dir makes it less likely.

### v2.5.0 (2018-06-17)

Changed:

* No longer separate multiline function defs from single-line function defs in Show command output.
* Use case-insensitive sort when sorting function names.
* Changed global function database from ``/home/<user>/.globalfunk`` to ``/home/<user>/.funky``.

Fixed:

* Creating a ``.funky`` file at ``/home/<user>`` would break ``chpwd()`` function, causing all
  global function overrides to persist until the end of the session even if the user changes back
  to the his/her home directory.

### v2.4.0 (2018-06-16)

Added:

* New VDEBUG ("verbose debug") logging level.
* ``--verbose`` option

  - Used with ``--debug`` it sets new VDEBUG logging level.
  - Used without any other options, the Show action command is run using verbose output. Going
    forward this will be used when sourcing function definitions.
  - Used with ``--help`` it unsuppresses any suppressed options (e.g. currently ``--global`` is
    normally suppressed).

Fixed:

* No longer unalias all single-letter funks automatically. Instead, functions/funks created
  with funky will automatically unalias function name before function definitions. (This
  requires the ``--verbose`` option to make visible in Show command output.)

### v2.3.5 (2018-06-12)

Fixed:

* Switching to another folder with local funks causes old local funks to continue to override
  global funks

### v2.3.4 (2018-06-12)

Fixed:

* Leaving a directory with local funks should unmask globalfunks.

  - Meaning that any global funks that were previously overridden should be back in scope.

### v2.3.3 (2018-06-12)

Fixed:

* Local funks were not consistently overriding global funks

### v2.3.2 (2018-06-12)

Fixed:

* Local database was not being deleted consistently when empty, as it should be.

### v2.3.1 (2018-06-12)

Fixed:

* Add (``-a``) and Edit (``-e``) commands now act more approriately when command definition is left
  blank.

### v2.3.0 (2018-06-12)

Changed:

* Local funks are now sourced into ``.zshrc``.

Removed:

* Execute command (``-x``). No longer needed now that funked are sourced directly into ``.zshrc``.
* Bash support

  - I wanted to focus on providing one service well. ZSH has some more advanced features than bash.
    Since I don't use bash, I'm not enthusiastic about supporting it. I'll reimplement it on
    request, but am not going to waste my time otherwise.

### v2.2.2 (2018-06-11)

Fixed:

* Using ``-x`` without argument should fail explicitly. (v2.2.1 did not resolve this issue as I had
  thought.)


### v2.2.1 (2018-06-11)

Fixed:

* Using ``-x`` without arguments should fail explicitly


### v2.2.0 (2018-06-10)

Added:

* Global funks (invoked with the ``--global`` option):

  - Global funks allow you to create default definitions for funks that can be overridden on
    a local basis.
  - All action commands still work properly when ``--global`` is used but they operate on the global
    database instead of the local one.

### v2.1.1 (2018-06-09)

Fixed:

* Dashed command-line arguments are not properly passed to command definition when a funk is
  executed.

### v2.1.0 (2018-06-09)

Added:

* New "rename" action command (``-R`` option).
* New ``--version`` option.

Changed:

* Remodeled argument parsing strategy. This remodel is mostly internal. A few actual changes in the
  API have taken place:

  - Options take arguments now, so the funk name must follow the action command.
  - The Show command no longer has an explicit option.
  - Long options have been removed.
    

### v2.0.6 (2018-06-07)

Fixed:

* Automatic command-line arguments are word-splitting for single-line funk definitions without
  param arguments.

### v2.0.5 (2018-06-06)

Fixed:

* Executed command's exit status not preserved (reintroduced this bug with v2.0.3).

### v2.0.4 (2018-06-06)

Fixed:

* Double printout of "command not found" message (caused by debug message left active in v2.0.3).

### v2.0.3 (2018-06-06)

Added:

* Bash support.

Changed:

* ``la`` is no longer an entry point. It is now only a recommended funk.
* funky.sh is now copied to ``$XDG_CONFIG_HOME/funky/funky.sh`` for easy access.
* funky.sh is now symlinked to oh-my-zsh custom plugin directory instead of being copied.

### v2.0.2 (2018-06-01)

Changed:

* Condensed show command output by grouping together single-line funk definitions.

Fixed:

* Funk arguments are handled intuitively again (without needing to explicitly append $@ to the definition).
* Automatic la funk on some systems blocks entry point. It is now unaliased at install time.
* Funk execution masks exit status.

### v2.0.1 (2018-05-31)

Fixed:

* Demonstration gif not working on PyPI project page.

### v2.0.0 (2018-05-31)

Migration from bash script prototype to python project and uploaded to PyPI.

### v1.0.0 (2018-03-18)

Prototype version. Funky bash script.
