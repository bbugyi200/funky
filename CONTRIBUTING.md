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

Ready to contribute? Here's how to setup `funky` for local development.

1. Fork the `funky` repo on GitHub.

2. Clone your fork locally:

    ```
    $ git clone git@github.com:your_name_here/funky.git
    ```

3. Install your local copy into a virtualenv. Assuming you have [virtualenvwrapper]
   installed, this is how you setup your fork for local development:

    ```
    $ cd funky/
    $ mkvirtualenv funky
    $ workon funky
    $ pip install -r dev-requirements.txt
    ```

4. Create a branch for local development:
    ``` 
    $ git checkout -b name-of-your-bugfix-or-feature
    ```
   Now you can make your changes locally.

5. When you're done making changes, check that all the tests are still passing::

    ``` 
    $ make check
    ```
    
   > **NOTE**: You must have [shunit2] installed to run the shell tests (e.g.  `test_funky.sh`)

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

8. Submit a pull request through GitHub.


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

[shunit2]: https://github.com/kward/shunit2
[virtualenvwrapper]: https://virtualenvwrapper.readthedocs.io/en/latest/index.html
