.. highlight:: shell

Usage
=====

Funks are manipulated using the ``funky`` command. The ``funky`` command can (perhaps
surpisingly) define not only local funks but global ones as well. The distinction between the two
is treated in the :ref:`usage-l-v-g` section below. But first, here are a list of the available 
command-line options (also viewable via the ``funky -h`` command):

.. argparse::
    :module: funky.app
    :func: _get_argparser
    :prog: funky
    :nodefaultconst:
    :nodescription:

Additional Notes
----------------

.. _usage-l-v-g:

Local vs Global
~~~~~~~~~~~~~~~

**Local** funks are stored using a hidden database file that is located in the same directory
where the funk was created. These can be manipulated using the action command options described
above. Once created, a local funk can be used just like any other command or normal funk---as
long as you have activated the provided shell extension (see :ref:`install-additional`) and are
inside of the directory where the local funk was originally defined.

**Global** funks, on the other hand, are stored in your home directory (``/home/<user>``) and can
be used from any directory. Local funks can be used to override global funk definitions.

Local and global funks can be manipulated (created, removed, edited, renamed, etc.) by using the
``funky`` and ``gfunky`` commands.

.. _usage-funcs:

Aliases vs Funks
~~~~~~~~~~~~~~~~~~~~

This project originally used funks. The decision to migrate to shell functions was made based on
the fact that shell functions are far more capable than funks. Moreover, there is very little
benefit to using aliases over shell functions.

With that said, actual aliases do have one appeal over shell functions. When you use an alias, any
arguments that you pass to it are automatically passed to the command definition (at runtime,
aliases are just substituted with their definitions). For the purpose of emulating this behavior
when it would typically be desired, a funk defined using a **single-line** command definition
that **does NOT already contain argument variables** (e.g. does not contain ``$0``, ``$1``, ...,
``$9``, ``$*``, or ``$@``) will automatically have the ``"$@"`` special parameter appended to its
definition. [#]_ This allows for the same automatic argument handling that you would expect from an
alias.

.. [#] See the official `Bash docs`_ for more information on Bash's special parameters.

.. _Bash docs: https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html 
.. _installation:
   https://funky.readthedocs.io/en/latest/installation.html#additional-steps-required

