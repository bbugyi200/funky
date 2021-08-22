# funky [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Funky%20makes%20ZSH%20shell%20functions%20more%20powerful%20and%20easier%20to%20manage&url=https://github.com/bbugyi200/funky&via=bryan_bugyi&hashtags=python,Linux,commandlineftw,developers)

**Funky takes shell functions to the next level by making them easier to define, more flexible, and more interactive.**

[![Project Version](https://img.shields.io/pypi/v/pyfunky)](https://pypi.org/project/pyfunky/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyfunky)](https://pypi.org/project/pyfunky/)
[![Package Health](https://snyk.io/advisor/python/pyfunky/badge.svg)](https://snyk.io/advisor/python/pyfunky)

[![Types: mypy](https://img.shields.io/badge/types-mypy-0606f5)](https://github.com/python/mypy)
[![pylint](https://img.shields.io/badge/linter-pylint-ffff00)](https://github.com/PyCQA/pylint)
[![flake8](https://img.shields.io/badge/linter-flake8-008080)](https://github.com/PyCQA/flake8)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/imports-isort-ef8336)](https://github.com/PyCQA/isort)

[![Test Workflow](https://github.com/bbugyi200/funky/actions/workflows/test.yml/badge.svg)](https://github.com/bbugyi200/funky/actions/workflows/test.yml)
[![Lint Workflow](https://github.com/bbugyi200/funky/actions/workflows/lint.yml/badge.svg)](https://github.com/bbugyi200/funky/actions/workflows/lint.yml)
[![Publish Workflow](https://github.com/bbugyi200/funky/actions/workflows/publish.yml/badge.svg)](https://github.com/bbugyi200/funky/actions/workflows/publish.yml)
[![Coverage](https://codecov.io/gh/bbugyi200/funky/branch/master/graph/badge.svg)](https://codecov.io/gh/bbugyi200/funky)

![demo]

## Table of Contents

* [Usage](#usage)
   * [Local vs Global](#local-vs-global)
   * [Funk Definition Shortcuts](#funk-definition-shortcuts)
      * [Special cd Funks](#special-cd-funks)
      * [Simulate Shell Variables](#simulate-shell-variables)
      * [The "$@" Special Parameter](#the--special-parameter)
* [Articles / Blog Posts](#articles--blog-posts)
* [Installation](#installation)
   * [Using pip to Install](#using-pip-to-install)
   * [Building from Source](#building-from-source)
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

## Articles / Blog Posts

With the goal of listing alternative sources of documentation / tutorials, this
section will be used to track any articles or blog posts which mention funky:

* [6 Command Line Tools for Productive Programmers](https://earthly.dev/blog/command-line-tools/#funky) (2021-07-23)


## Installation

### Using `pip` to Install

To install funky, run the following commands in your terminal (replace `SHELL`
with either `bash` or `zsh`):

``` shell
python3 -m pip install --user pyfunky  # install funky
python3 -m funky --setup-shell SHELL  # hook funky into your shell
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

The last thing you need to do is hook funky into your shell of choice, which
can be accomplished with the following command (replace `SHELL` with either
`bash` or `zsh`):

```shell
python3 -m funky --setup-shell SHELL
```

## Similar Projects

* [desk](https://github.com/jamesob/desk) - A lightweight workspace manager for the shell.
* [smartcd](https://github.com/cxreg/smartcd) - Alter your bash (or zsh) environment as you cd.
* [direnv](https://github.com/direnv/direnv) - is an extension for your shell. It augments existing shells with a new feature that can load and unload environment variables depending on the current directory.


## Contributions

Pull requests are welcome. See [CONTRIBUTING.md](https://github.com/bbugyi200/funky/blob/master/CONTRIBUTING.md) for more information.

[logo]: https://raw.githubusercontent.com/bbugyi200/funky/master/img/logo-96.png
[travis]: https://travis-ci.org/bbugyi200/funky.svg?branch=master
[codecov]: https://codecov.io/gh/bbugyi200/funky/branch/master/graph/badge.svg
[demo]: https://raw.githubusercontent.com/bbugyi200/funky/master/img/demo.gif "Funky Demonstration GIF"
[Github repo]: https://github.com/bbugyi200/funky
[tarball]: https://github.com/bbugyi200/funky/tarball/master
