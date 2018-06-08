Usage
=====
 
.. argparse::
    :module: localalias.app
    :func: _get_argparser
    :prog: localalias
    :nodefaultconst:
    :nodescription:

    Local aliases can be created (-a) and edited (-e) using the ``localalias`` command.  All
    aliases are stored using a hidden database file that is located in the same directory where the
    alias was created. Once created, a local alias can be used just like any other command or
    normal alias, as long as you have activated the provided shell extension (see
    :ref:`install-additional`).

Additional Notes
----------------

Use ``la`` over ``localalias``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I strongly recommend against using the ``localalias`` command in its full form. It is preferrable
to set an alias such as 

.. code-block:: shell

   alias la='localalias --color'

and use that in place of the official command. One of the primary goals of this project is to
reduce keystrokes, so advocating the frequent use of a 10-letter command wouldn't make much sense.

Aliases vs Functions
~~~~~~~~~~~~~~~~~~~~

Note that while this documentation (and the project's name) refers to the command definitions
created by ``la`` as "aliases", they actually behave more like shell functions. This makes them
much more powerful. Namely, this means you can use them with arguments.

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

