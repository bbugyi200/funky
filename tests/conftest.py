"""Shared fixture file used by pytest.

https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files
"""

import os
from pathlib import Path
from typing import Iterator

from _pytest.tmpdir import TempPathFactory
from pytest import fixture


@fixture
def xdg_data_home(tmp_path_factory: TempPathFactory) -> Iterator[Path]:
    """Yields a temporary XDG_DATA_HOME directory.

    NOTE: The XDG_DATA_HOME envvar will be set accordingly until this fixture's
    teardown.
    """
    result = tmp_path_factory.mktemp("xdg_data")
    old_data_dir = os.environ.get("XDG_DATA_HOME", None)
    os.environ["XDG_DATA_HOME"] = str(result)

    yield result

    if old_data_dir:
        os.environ["XDG_DATA_HOME"] = old_data_dir
    else:
        del os.environ["XDG_DATA_HOME"]
