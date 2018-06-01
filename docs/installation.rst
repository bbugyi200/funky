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

Additional Steps Required
-------------------------

For the best experience, localalias needs to be integrated into your preferred shell environment
using a shell script/plugin. There are multiple ways to achieve this.

zsh
^^^

A shell script by the name of ``localalias.zsh`` should have been included with the installation
(it can also be found `here`__).  If you use `oh-my-zsh`_, the easiest way to enable this
script is by adding it as a plugin. You should be able to accomplish this simply by adding
localalias to your list of plugins, which can be found in your ``.zshrc`` file. If you were only
using the ``foo`` and ``bar`` plugins before installing localalias, for example, you would change
the plugins line from

__  https://github.com/bbugyi200/localalias/blob/master/scripts/zsh/localalias.zsh

.. code-block:: shell

   plugins=(foo bar)

to

.. code-block:: shell

   plugins=(foo bar localalias)

See oh-my-zsh's `documentation <https://github.com/robbyrussell/oh-my-zsh/wiki/Customization/>`_
for more information.


.. important::
   If you have `oh-my-zsh`_ installed, the ``localalias.zsh`` file should have been automatically
   copied to 

   .. code-block:: shell

        $ZSH_CUSTOM/plugins/localalias/localalias.plugin.zsh

   during the installation process.  If for some reason this failed to occur, however, you **must**
   perform this step manually or the plugin will NOT work.


If you do NOT have `oh-my-zsh`_ installed, you can simply copy ``localalias.zsh`` to a location of
your choosing and source it into your ``.zshrc`` file. For example, assuming you chose to copy
the file to ``~/.zsh``, you would add the following line to your ``.zshrc``:

.. code-block:: shell

   source ~/.zsh/localalias.zsh

.. _oh-my-zsh: https://github.com/robbyrussell/oh-my-zsh

bash
^^^^

Bash is not yet officially supported. A bash equivalent to ``localalias.zsh`` should be very simple
to implement on your own, however, as long as you are atleast vaguely familiar with bash scripting.
