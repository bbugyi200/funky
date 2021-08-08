# funky [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Funky%20makes%20ZSH%20shell%20functions%20more%20powerful%20and%20easier%20to%20manage&url=https://github.com/bbugyi200/funky&via=bryan_bugyi&hashtags=python,Linux,commandlineftw,developers)

**Funky takes shell functions to the next level by making them easier to define, more flexible, and more interactive.**

[![Test Workflow](https://github.com/bbugyi200/funky/actions/workflows/test.yml/badge.svg)](https://github.com/bbugyi200/funky/actions/workflows/test.yml)
[![Lint Workflow](https://github.com/bbugyi200/funky/actions/workflows/lint.yml/badge.svg)](https://github.com/bbugyi200/funky/actions/workflows/lint.yml)
[![Publish Workflow](https://github.com/bbugyi200/funky/actions/workflows/publish.yml/badge.svg)](https://github.com/bbugyi200/funky/actions/workflows/publish.yml)
[![Coverage](https://codecov.io/gh/bbugyi200/funky/branch/master/graph/badge.svg)](https://codecov.io/gh/bbugyi200/funky)
[![Version](https://img.shields.io/pypi/v/pyfunky)](https://pypi.org/project/pyfunky/)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

![demo]

## Table of Contents

* [Usage](#usage)
   * [Local vs Global](#local-vs-global)
   * [Funk Definition Shortcuts](#funk-definition-shortcuts)
      * [Special cd Funks](#special-cd-funks)
      * [Simulate Shell Variables](#simulate-shell-variables)
      * [The "$@" Special Parameter](#the--special-parameter)
* [Installation](#installation)
   * [Using pip to Install](#using-pip-to-install)
   * [Building from Source](#building-from-source)
   * [Additional Installation Steps](#additional-installation-steps)
* [Similar Projects](#similar-projects)
* [Contributions](#contributions)

## Usage
Funks are manipulated using the `funky` and `gfunky` commands. These commands have the same user interface, which is specified in the [Command-line Interface](#command-line-interface) section. The difference between the two commands is treated in the [Local vs Global](#local-vs-global) section.

### Local vs Global

**Local** funks are stored using a hidden database file that is located in the same directory
where the funk was created. These can be manipulated using the action command options described
above. Once created, a local funk can be used just like any other command or normal funk---as
long as you have activated the provided shell extension (see [Additional Install Steps](#additional-installation-steps)) and are
inside of the directory where the local funk was originally defined.

**Global** funks, on the other hand, are stored in your home directory (``/home/<user>``) and can
be used from any directory. Local funks can be used to override global funk definitions.

Local and global funks can be manipulated (created, removed, edited, renamed, etc.) by using the
``funky`` and ``gfunky`` commands, respectively.

### Funk Definition Shortcuts

Normally when defining a funk, the provided raw definition (the final contents of the temp file) is inserted directly into the generated function definition. However, funky does try to make some alterations to the original funk definition when doing so is convenient. These *funky definition shortcuts* can make defining funks faster:

#### Special `cd` Funks

A funk definition of the form `@./relative/path/to/directory` will be automatically changed to

``` bash
cd /absolute/path/to/directory/"$@" || return 1
```

#### Simulate Shell Variables

A funk definition of the form `"Some string here..."` will be automatically changed to

``` bash
echo "Some string here..." "$@"
```

This allows you to use funks to simulate shell variables via [command substitution](https://www.gnu.org/software/bash/manual/html_node/Command-Substitution.html).

#### The "$@" Special Parameter

This project originally used aliases. The decision to migrate to shell functions was made based on
the fact that shell functions are far more capable than aliases. Moreover, there is very little
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

### Using `pip` to Install

To install funky, run this command in your terminal:

``` shell
$ pip install pyfunky
```

This is the preferred method to install funky, as it will always install the most recent stable release.

If you don't have [pip] installed, this [Python installation guide] can guide
you through the process.

[pip]: https://pip.pypa.io
[Python installation guide]: http://docs.python-guide.org/en/latest/starting/installation/


### Building from Source

You can either clone the public repository:

``` shell
$ git clone git://github.com/bbugyi200/funky
```

Or download the [tarball]:

``` shell
$ curl  -OL https://github.com/bbugyi200/funky/tarball/master
```

Once you have a copy of the source, you can install funky by running:

``` shell
make install
```

### Additional Installation Steps

For the best experience, funky needs to be integrated into your shell environment using the
provided shell script.

A shell script by the name of `funky.sh` should have been copied to

``` shell
$XDG_DATA_HOME/funky/funky.sh
```

during the installation process (it can also be found [here][funky.sh]).  You can integrate funky into your shell by sourcing the `funky.sh` script into your shell's configuration file. Assuming the script was copied to `~/.local/share/funky/funky.sh` (its default location), for example, you would add the following line to your `.zshrc` OR `bashrc`:

``` shell
[ -f ~/.local/share/funky/funky.sh ] && source ~/.local/share/funky/funky.sh
```

If you install funky with root permissions, the ``funky.sh`` script will instead be installed to ``/usr/share/funky/funky.sh``.

## Similar Projects

* [desk](https://github.com/jamesob/desk) - A lightweight workspace manager for the shell
* [smartcd](https://github.com/cxreg/smartcd) - Alter your bash (or zsh) environment as you cd


## Contributions

Pull requests are welcome. See [CONTRIBUTING.md](https://github.com/bbugyi200/funky/blob/master/CONTRIBUTING.md) for more information.

[logo]: https://raw.githubusercontent.com/bbugyi200/funky/master/img/logo-96.png
[travis]: https://travis-ci.org/bbugyi200/funky.svg?branch=master
[codecov]: https://codecov.io/gh/bbugyi200/funky/branch/master/graph/badge.svg
[demo]: https://raw.githubusercontent.com/bbugyi200/funky/master/img/demo.gif "Funky Demonstration GIF"
[funky.sh]:  https://github.com/bbugyi200/funky/blob/master/scripts/shell/funky.sh
[Github repo]: https://github.com/bbugyi200/funky
[tarball]: https://github.com/bbugyi200/funky/tarball/master
