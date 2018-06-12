.. highlight:: shell

Usage
=====

.. note::
        
    Throughout the rest of this document, the term *alias* will be thrown around a lot (shocker,
    right?). It is important to first understand, however, that when we use the term *alias* we
    refer to a command defined with the use of the ``localalias`` command. These are not aliases
    but shell functions. Little functionality is lost by using shell functions over aliases, but
    much is gained (see :ref:`usage-funcs`).

Aliases are manipulated using the ``localalias`` command. The ``localalias`` command can (perhaps
surpisingly) define not only local aliases but global ones as well. The distinction between the two
is treated in the :ref:`usage-l-v-g` section below. But first, here are a list of the available 
command-line options (also viewable via the ``localalias -h`` command):

.. argparse::
    :module: localalias.app
    :func: _get_argparser
    :prog: localalias
    :nodefaultconst:
    :nodescription:

Additional Notes
----------------

.. _usage-l-v-g:

Local vs Global
~~~~~~~~~~~~~~~

**Local** aliases are stored using a hidden database file that is located in the same directory
where the alias was created. These can be manipulated using the action command options described
above. Once created, a local alias can be used just like any other command or normal alias---as
long as you have activated the provided shell extension (see :ref:`install-additional`) and are
inside of the directory where the local alias was originally defined.

**Global** aliases, on the other hand, are stored in your home directory (``/home/<user>``) and can
be used from any directory. Local aliases can be used to override global alias definitions.

Local and global aliases can be manipulated (created, removed, edited, renamed, etc.) by using the
``la`` and ``al`` commands described in :ref:`usage-la-al`.

.. _usage-la-al:

Use ``la`` and ``al`` over ``localalias``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two helper functions, ``la`` and ``al``, are defined during installation.  It is recommended that
these functions be used in place of the standard ``localalias`` command. ``la`` acts as a wrapper
for ``localalias --color``, whereas ``al`` acts as a wrapper for ``localalias --color --global``.
After using either of these helper functions, any newly created or altered aliases will be sourced
into your current shell environment so they will be ready for immediate use.

.. _usage-funcs:

Aliases vs Functions
~~~~~~~~~~~~~~~~~~~~

Note that while this documentation (and the project's name) refers to the command definitions
created by ``localalias`` as "aliases", they are actually shell functions. This makes them
much more powerful. Namely, this means you can use them with arguments.

This project originally used aliases. The decision to migrate to shell functions was made based on
the fact that shell functions are far more capable than aliases. Moreover, there is very little
benefit to using aliases over shell functions.

With that said, actual aliases do have one appeal over shell functions. When you use an alias, any
arguments that you pass to it are automatically passed to the command definition (at runtime,
aliases are just substituted with their definitions). For the purpose of emulating this behavior
when it would typically be desired, an alias defined using a **single-line** command definition
that **does NOT already contain argument variables** (e.g. does not contain ``$0``, ``$1``, ...,
``$9``, ``$*``, or ``$@``) will automatically have the ``"$@"`` special parameter appended to its
definition. [#]_ This allows for the same automatic argument handling that you would expect from an
actual alias.

.. [#] See the official `Bash docs`_ for more information on Bash's special parameters.

.. _Bash docs: https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html 
.. _installation:
   https://localalias.readthedocs.io/en/latest/installation.html#additional-steps-required

