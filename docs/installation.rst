.. highlight:: shell

.. _install:

============
Installation
============


Using ``pip`` to Install
------------------------

To install funky, run this command in your terminal:

.. code-block:: console

    $ pip install funky

This is the preferred method to install funky, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Building from Source
--------------------

The sources for funky can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/bbugyi200/funky

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/bbugyi200/funky/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/bbugyi200/funky
.. _tarball: https://github.com/bbugyi200/funky/tarball/master

.. _install-additional:

Additional Installation Steps
-----------------------------

For the best experience, funky needs to be integrated into your shell environment using the
provided shell script.

.. _install-manual:

Manual Integration
~~~~~~~~~~~~~~~~~~

A shell script by the name of ``funky.zsh`` should have been copied to

.. code-block:: shell

   $XDG_DATA_HOME/funky/funky.zsh

during the installation process (it can also be found `here`__).  You can integrate funky into
your shell by sourcing the ``funky.zsh`` script into your shell's configuration file. Assuming
the script was copied to ``~/.local/share/funky/funky.zsh`` (its default location), for
example, you would add the following line to your ``.zshrc``:

.. code-block:: shell

   [ -f ~/.local/share/funky/funky.zsh ] && source ~/.local/share/funky/funky.zsh

.. note::

  If you install funky with root permissions, the ``funky.zsh`` script will instead be
  installed to ``/usr/share/funky/funky.zsh``.

__  https://github.com/bbugyi200/funky/blob/master/scripts/zsh/funky.zsh
.. _oh-my-zsh: https://github.com/robbyrussell/oh-my-zsh
