# How do I run the tests?

Funky uses two different types of tests:

* Python tests, which test funky's core codebase. These tests use the [pytest] framework.
* Shell tests, which test the shell integration script. These tests use the [shunit2] framework.

## Python Tests

The Python tests can be run using the following command: `runtests`

## Shell Tests

The Shell tests can be run using the following command: `./scripts/shell/test_funky.sh`.

## Running ALL Tests

The easiest way to run all tests is to use the `make check` command.


[pytest]: https://github.com/pytest-dev/pytest
[shunit2]: https://github.com/kward/shunit2
