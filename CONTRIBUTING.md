# Contributing

## How to submit feedback?

The best way to send feedback is to [file an issue](https://github.com/bbugyi200/funky/issues).

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Setup funky for Local Development

Ready to contribute? Here are the steps required to setup funky for local
development.

1. Fork the funky repo on GitHub.

1. Clone your fork locally:

    ```console
    $ git clone git@github.com:your_name_here/funky.git
    ```

1. Install your local copy of funky and all of funky's Python development
   dependencies into a virtualenv. Assuming you have [virtualenvwrapper]
   installed, the following commands should do the trick:

    ```console
    $ cd funky/
    $ mkvirtualenv funky
    $ python setup.py develop
    $ pip install -r dev-requirements.txt
    ```
    
1. Install system development dependencies (e.g. [shunit2]):
   
   ```console
   $ ./scripts/install-system-dev-deps
   ```

1. Create a branch for local development:

    ``` console
    $ git checkout -b name-of-your-bugfix-or-feature
    ```

   Now you can make your changes locally.

1. When you're done making changes, check that all the tests are still passing::

    ```console
    $ make test
    ```

1. Additionally, any code added / changed is expected to pass all linting checks.

   ```console
   $ make lint
   ```

1. Commit your changes and push your branch to GitHub:

    ```console
    $ git add .
    $ git commit -m "Detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```

1. Submit a pull request through GitHub.


## Deploying

A reminder for the maintainers on how to deploy. Make sure all your changes
are committed and that you have [bumpversion] installed. Then run:

```console
$ bumpversion patch  # possible values: major / minor / patch
$ git push
$ git push --tags
```

A new version of funky will then deploy to PyPI if tests pass.

[bumpversion]: https://github.com/c4urself/bump2version
[shunit2]: https://github.com/kward/shunit2
[virtualenvwrapper]: https://virtualenvwrapper.readthedocs.io/en/latest/index.html
