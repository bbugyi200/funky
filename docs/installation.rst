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
using a shell script/plugin. The ideal way to achieve this is through the use of `oh-my-zsh`_'s
plugin functionality; however, you may also source the provided shell extension directly into your
shell's configuration file. Both of these methods are described in more detail below.

Oh-My-Zsh Plugin
~~~~~~~~~~~~~~~~

If you use `oh-my-zsh`_, the easiest way to integrate localalias into your shell is by enabling the
``localalias`` plugin. You should be able to accomplish this simply by adding ``localalias`` to
your list of plugins, which can usually be found in your ``.zshrc`` file. If you were only using
the ``foo`` and ``bar`` plugins before installing localalias, for example, you would change the
plugins line from

.. code-block:: shell

   plugins=(foo bar)

to

.. code-block:: shell

   plugins=(foo bar localalias)

See oh-my-zsh's `documentation <https://github.com/robbyrussell/oh-my-zsh/wiki/Customization/>`_
for more information.


.. important:: 
    
   If you have `oh-my-zsh`_ installed, a symbolic link should have been created from  the
   ``localalias.zsh`` script---described in the :ref:`install-manual` section---to 

   .. code-block:: shell

        $ZSH_CUSTOM/plugins/localalias/localalias.plugin.zsh

   during the installation process.  If for some reason this failed to occur, however, you **must**
   perform this step manually or the plugin will NOT work. On most systems, this can be achieved by
   running the following commands in sequence:

   .. code-block:: shell

        mkdir ~/.oh-my-zsh/custom/plugins/localalias        
        ln -s ~/.config/localalias/localalias.zsh ~/.oh-my-zsh/custom/plugins/localalias/localalias.plugin.zsh         

.. _install-manual:

Manual Integration
~~~~~~~~~~~~~~~~~~

A shell script by the name of ``localalias.zsh`` should have been copied to

.. code-block:: shell

   $XDG_CONFIG_HOME/localalias/localalias.zsh

during the installation process (it can also be found `here`__). If you do NOT have `oh-my-zsh`_
installed, you can integrate localalias into your shell by sourcing the ``localalias.zsh`` script
into your shell's configuration file. Assuming the script was copied to
``~/.config/localalias/localalias.zsh`` (its default location), for example, you would add the
following line to your ``.zshrc``:

.. code-block:: shell

   source ~/.config/localalias/localalias.zsh


__  https://github.com/bbugyi200/localalias/blob/master/scripts/zsh/localalias.zsh
.. _oh-my-zsh: https://github.com/robbyrussell/oh-my-zsh
