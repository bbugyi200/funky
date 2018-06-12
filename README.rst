==========
localalias
==========

*Don't kill your fingers by typing out long commands! Local aliases can help you achieve a whole
new level of lazy!*

.. image:: https://travis-ci.org/bbugyi200/localalias.svg?branch=master
    :target: https://travis-ci.org/bbugyi200/localalias

.. image:: https://codecov.io/gh/bbugyi200/localalias/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/bbugyi200/localalias

.. image:: https://readthedocs.org/projects/localalias/badge/?version=latest&style=flat
   :target: https://localalias.readthedocs.io/en/latest/?badge=latest

Demonstration
-------------

.. image:: https://github.com/bbugyi200/localalias/blob/master/docs/img/demo.gif?raw=true

NOTE: This demonstration uses the `helper function`__, ``la``, in place of the standard
``localalias`` command.

__ https://localalias.readthedocs.io/en/latest/usage.html#use-la-and-al-over-localalias

Description
-----------

localalias is **a light-weight shell wrapper that allows you to create per-directoy command
aliases.**

With bash/zsh, once an alias is set, it cannot be reused. If you want to define a new command using
an alias, you have to choose a new alias name. This forces you to define many aliases, some of them
with very obscure names that you will never remember. localalias solves this problem by
providing an additional level of abstraction to your shell's default alias design scheme.

Local aliases allow you to abstract away from whatever project you are working on, by giving you
the ability to setup generic aliases for what are, in actuality, very specific tasks. In my own
setup, for example, I alias ``r`` to the command that launches the project I am working on. When in
the top-level directory of the localalias project directory, running ``r`` is equivalent to
``python localalias``.  If I change directories, however, to work on a different project, running
``r`` will run a different command---one corresponding to the new project.  I use multiple patterns
like this to simplify my own workflow: ``t`` runs the tests, ``b`` builds the project, ``v`` opens
up files in ``vim``. [#]_

.. [#] I normally use multiple variations of this last one: ``v`` opens up the most active files
   (the ones I am most likely to want to edit), ``vt`` opens up test files, ``vd`` opens up doc
   files, etc..

.. inclusion-marker-do-not-remove

Documentation
-------------

For more information, please refer to this project's official `documentation`_.

There you will also find instructions for `installation`_ and tips for general `usage`_.

.. _documentation: https://localalias.readthedocs.io
.. _installation: https://localalias.readthedocs.io/en/latest/installation.html
.. _usage: https://localalias.readthedocs.io/en/latest/usage.html
