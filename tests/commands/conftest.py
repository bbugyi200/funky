import collections
import json
import os
import tempfile

import pytest

from localalias import commands


@pytest.fixture
def cleandir():
    """Run tests in an empty directory."""
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)


@pytest.fixture
def alias_dict():
    alias_dict = {'multiline': 'echo "Hello"\necho "world!"',
                  'run': 'python main.py',
                  'T': 'pytest test_main.py'}
    return alias_dict


@pytest.fixture
def fake_db(alias_dict):
    """Setup/teardown a local alias database."""
    filename = commands.Command.LOCALALIAS_DB_FILENAME
    with open(filename, 'w') as f:
        json.dump(alias_dict, f)
    yield alias_dict
    try:
        os.remove(filename)
    except FileNotFoundError as e:
        pass


@pytest.fixture(params=[
    ('run', False),
    ('multiline', False),
], ids=['run', 'multiline'])
def cmd_args(request):
    """Returns a named tuple of command arguments and expected results."""
    Args = collections.namedtuple('Args', ['alias', 'color'])
    args = Args(request.param[0], request.param[1])
    return args
