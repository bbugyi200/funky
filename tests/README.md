# How do I run the tests?

Funky uses two different types of tests:

* **Python tests**, which test funky's core codebase. These tests use the [pytest] framework and can be run using the `make test-python` command. You may specify `pytest` command-line options by setting the `pytest_opts` variable (e.g. `make test-python pytest_opts=-v`).
* **Shell tests**, which test the shell integration script. These tests use the [shunit2] framework and can be run using the `make test-shell` command.

You can **run all the tests** using the `make test` command.


# Debugging with pdb/pudb

Simply running `pudb funky/__main__.py` will cause the relative imports within the codebase to fail. Instead, you must explicitly tell funky that you wish to debug it. This can be accomplished, for example, with the following command:
``` bash
DEBUG_FUNKY=1 pudb funky/__main__.py
```


[pytest]: https://github.com/pytest-dev/pytest
[shunit2]: https://github.com/kward/shunit2
