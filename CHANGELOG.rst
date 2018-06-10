==========
Change Log
==========

All notable changes to this project will be documented in this file. This project adheres to
`Semantic Versioning <http://semver.org/>`_, though minor breaking changes can happen in minor
releases.

v2.2.0 (Unreleased)
-------------------

Added:

* Global aliases (invoked with the ``-g`` option):

  - Global aliases allow you to create default definitions for aliases that can be overridden on
    a local basis.
  - All action commands still work properly when ``-g`` is used but they operate on the global
    database instead of the local one.

v2.1.1 (2018-06-09)
-------------------

Fixed:

* Dashed command-line arguments are now properly passed to command definition when an alias is
  executed.

v2.1.0 (2018-06-09)
-------------------

Added:

* New "rename" action command (``-R`` option).
* New ``--version`` option.

Changed:

* Remodeled argument parsing strategy. This remodel is mostly internal. A few actual changes in the
  API have taken place:

  - Options take arguments now, so the alias name must follow the action command.
  - The Show command no longer has an explicit option.
  - Long options have been removed.
    

v2.0.6 (2018-06-07)
-------------------

Fixed:

* Automatic command-line arguments are no longer word-splitting for single-line alias definitions
  without param arguments.

v2.0.5 (2018-06-06)
-------------------

Fixed:

* Executed command's exit status not preserved (reintroduced this bug with v2.0.3).

v2.0.4 (2018-06-06)
-------------------

Fixed:

* Double printout of "command not found" message (caused by debug message left active in v2.0.3).

v2.0.3 (2018-06-06)
-------------------

Added:

* Bash support.

Changed:

* ``la`` is no longer an entry point. It is now only a recommended alias.
* localalias.sh is now copied to ``$XDG_CONFIG_HOME/localalias/localalias.sh`` for easy access.
* localalias.sh is now symlinked to oh-my-zsh custom plugin directory instead of being copied.

v2.0.2 (2018-06-01)
-------------------

Changed:

* Condensed show command output by grouping together single-line alias definitions.

Fixed:

* Alias arguments are handled intuitively again (without needing to explicitly append $@ to the definition).
* Automatic la alias on some systems blocks entry point. It is now unaliased at install time.
* Alias execution no longer masks exit status.

v2.0.1 (2018-05-31)
-------------------

Fixed:

* Repaired demonstration gif for PyPI project page.

v2.0.0 (2018-05-31)
-------------------

Migration from bash script prototype to python project and uploaded to PyPI.

v1.0.0 (2018-03-18)
-------------------

Prototype version. LocalAlias bash script.
