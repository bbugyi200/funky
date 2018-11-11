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

## Get Started!

Ready to contribute? Here's how to set up `funky` for local development.

1. Fork the `funky` repo on GitHub.
2. Clone your fork locally:
    ```
    $ git clone git@github.com:your_name_here/funky.git
    ```
3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development:
    ```
    $ mkvirtualenv funky
    $ cd funky/
    $ python setup.py develop
    ```
4. Create a branch for local development:
    ``` 
    $ git checkout -b name-of-your-bugfix-or-feature
    ```
   Now you can make your changes locally.
5. When you're done making changes, check that all the tests are still passing::
    ``` 
    $ python setup.py test or py.test
    ```
6. Additionally, any code added / changed is expected to meet flake8 style guidelines.
   Make sure by running::
   ``` 
   $ flake8 funky tests
   ```
7. Commit your changes and push your branch to GitHub::
    ``` 
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```
8. Submit a pull request through the GitHub website.

## Pull Request Guidelines

The pull request should work for Python 3.4, 3.5 and 3.6, and for PyPy. Check
[Travis CI](https://travis-ci.org/bbugyi200/funky/pull_requests) and make sure that the tests pass for all
supported Python versions.

In addition, for all code contributions excluding bugfixes, it is expected that the documentation
has been updated and/or additional documentation has been added.

Furthermore, additional tests should be created before submitting any major changes to the
codebase.


## Deploying

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed.
Then run:

``` 
$ bumpversion patch # possible: major / minor / patch
$ git push
$ git push --tags
```

Travis will then deploy to PyPI if tests pass.
