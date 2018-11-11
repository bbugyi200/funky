# funky

![logo] **Funky makes ZSH shell functions more powerful and easier to manage.**

![travis] ![codecov]

![demo]

## Usage

Funks are manipulated using the `funky` and `gfunky` commands. The distinction between the two is
treated in the [Local vs Global](#lvg) section below.

#### <a name="lvg">Local vs Global</a>

**Local** funks are stored using a hidden database file that is located in the same directory
where the funk was created. These can be manipulated using the action command options described
above. Once created, a local funk can be used just like any other command or normal funk---as
long as you have activated the provided shell extension (see :ref:`install-additional`) and are
inside of the directory where the local funk was originally defined.

**Global** funks, on the other hand, are stored in your home directory (``/home/<user>``) and can
be used from any directory. Local funks can be used to override global funk definitions.

Local and global funks can be manipulated (created, removed, edited, renamed, etc.) by using the
``funky`` and ``gfunky`` commands, respectively.

#### Aliases vs Funks

This project originally used funks. The decision to migrate to shell functions was made based on
the fact that shell functions are far more capable than funks. Moreover, there is very little
benefit to using aliases over shell functions.

With that said, actual aliases do have one appeal over shell functions. When you use an alias, any
arguments that you pass to it are automatically passed to the command definition (at runtime,
aliases are just substituted with their definitions). For the purpose of emulating this behavior
when it would typically be desired, a funk defined using a **single-line** command definition
that **does NOT already contain argument variables** (e.g. does not contain `$0`, `$1`, ...,
`$9`, `$*`, or `$@`) will automatically have the `"$@"` special parameter appended to its
definition. This allows for the same automatic argument handling that you would expect from an
alias.

See the official [Bash docs] for more information on Bash's special parameters.

[Bash docs]: https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html 


## Installation

#### Using `pip` to Install

To install funky, run this command in your terminal:

``` shell
$ pip install pyfunky
```

This is the preferred method to install funky, as it will always install the most recent stable release.

If you don't have [pip] installed, this [Python installation guide] can guide
you through the process.

[pip]: https://pip.pypa.io
[Python installation guide]: http://docs.python-guide.org/en/latest/starting/installation/


#### Building from Source

You can either clone the public repository:

``` shell
$ git clone git://github.com/bbugyi200/funky
```

Or download the [tarball]:

``` shell
$ curl  -OL https://github.com/bbugyi200/funky/tarball/master
```

Once you have a copy of the source, you can install it with:

``` shell
$ python setup.py install
```

#### Additional Installation Steps

For the best experience, funky needs to be integrated into your shell environment using the
provided shell script.

A shell script by the name of `funky.zsh` should have been copied to

``` shell
$XDG_DATA_HOME/funky/funky.zsh
```

during the installation process (it can also be found [here][funky.zsh]).  You can integrate funky into your shell by sourcing the `funky.zsh` script into your shell's configuration file. Assuming the script was copied to `~/.local/share/funky/funky.zsh` (its default location), for example, you would add the following line to your `.zshrc`:

``` shell
[ -f ~/.local/share/funky/funky.zsh ] && source ~/.local/share/funky/funky.zsh
```

If you install funky with root permissions, the ``funky.zsh`` script will instead be installed to ``/usr/share/funky/funky.zsh``.


## Contributions

Pull requests are welcome. See [CONTRIBUTING.md](https://github.com/bbugyi200/funky/blob/master/CONTRIBUTING.md) for more information.

[logo]: https://raw.githubusercontent.com/bbugyi200/funky/master/img/logo-96.png
[travis]: https://travis-ci.org/bbugyi200/funky.svg?branch=master
[codecov]: https://codecov.io/gh/bbugyi200/funky/branch/master/graph/badge.svg
[demo]: https://raw.githubusercontent.com/bbugyi200/funky/master/img/demo.gif
[funky.zsh]:  https://github.com/bbugyi200/funky/blob/master/scripts/zsh/funky.zsh
[Github repo]: https://github.com/bbugyi200/funky
[tarball]: https://github.com/bbugyi200/funky/tarball/master
