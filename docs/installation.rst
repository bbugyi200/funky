.. highlight:: shell

.. _install:

============
Installation
============


Using ``pip`` to Install
------------------------

To install localalias, run this command in your terminal:

.. code-block:: console

    $ pip install localalias

This is the preferred method to install localalias, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Building from Source
--------------------

The sources for localalias can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/bbugyi200/localalias

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/bbugyi200/localalias/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/bbugyi200/localalias
.. _tarball: https://github.com/bbugyi200/localalias/tarball/master

.. _install-additional:

Additional Installation Steps
-----------------------------

For the best experience, localalias needs to be integrated into your preferred shell environment
using a shell script/plugin.

.. _install-manual:

Manual Integration
~~~~~~~~~~~~~~~~~~

A shell script by the name of ``localalias.zsh`` should have been copied to

.. code-block:: shell

   $XDG_DATA_HOME/localalias/localalias.zsh

during the installation process (it can also be found `here`__).  You can integrate localalias into
your shell by sourcing the ``localalias.zsh`` script into your shell's configuration file. Assuming
the script was copied to ``~/.local/share/localalias/localalias.zsh`` (its default location), for
example, you would add the following line to your ``.zshrc``:

.. code-block:: shell

   [ -f ~/.local/share/localalias/localalias.zsh ] && source ~/.local/share/localalias/localalias.zsh

.. note::

  If you install localalias with root permissions, the ``localalias.zsh`` script will instead be
  installed to ``/usr/share/localalias/localalias.zsh``.

__  https://github.com/bbugyi200/localalias/blob/master/scripts/zsh/localalias.zsh
.. _oh-my-zsh: https://github.com/robbyrussell/oh-my-zsh
