# How do I run the tests?

Funky uses two different types of tests:

* Python tests, which test funky's core codebase. These tests use the [pytest] framework and can be run by using the `make check-python` command.
* Shell tests, which test the shell integration script. These tests use the [shunit2] framework and can be run by using the `make check-shell` command.

You can **run all the tests** using the `make check` command.


[pytest]: https://github.com/pytest-dev/pytest
[shunit2]: https://github.com/kward/shunit2
