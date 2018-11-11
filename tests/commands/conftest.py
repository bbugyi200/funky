import collections
import json
import os
import shutil
import tempfile
import unittest.mock as mock

import pytest

from funky import commands


@pytest.fixture
def cleandir():
    """Run tests in an empty directory."""
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
    yield
    shutil.rmtree(newpath)


@pytest.fixture
def setup_edit_patches():
    """Setup sp and tempfile patches for testing edit and add commands."""
    def _patch_edit(sp, tempfile, cmd_string):
        tmpfilename = '/tmp/test_edit.txt'
        with open(tmpfilename, 'w') as f:
            f.write(cmd_string)

        fileMock = mock.Mock(name='fileMock')
        fileMock.name = tmpfilename
        tempfile.NamedTemporaryFile = mock.Mock()
        tempfile.NamedTemporaryFile.return_value = fileMock
    return _patch_edit


@pytest.fixture
def fake_global_db(global_filename):
    """Setup/teardown a global funk database"""
    _fake_db = _fake_db_factory(global_filename, global_funk_dict)
    yield from _fake_db()


@pytest.fixture
def global_filename():
    """Returns a fake global database path so the production global db is not overwritten."""
    return "/tmp/.globalfunk"


@pytest.fixture
def fake_db(funk_dict):
    """Setup/teardown a local funk database"""
    _fake_db = _fake_db_factory(commands.Command.FUNKY_DB_FILENAME, funk_dict)
    yield from _fake_db()


def _fake_db_factory(DB_FILENAME, funk_dict_builder):
    """Builds a generator fixture for creating a fake database."""
    def _fake_db():
        my_funk_dict = funk_dict_builder
        with open(DB_FILENAME, 'w') as f:
            json.dump(my_funk_dict, f)
        yield my_funk_dict
        try:
            os.remove(DB_FILENAME)
        except FileNotFoundError:
            pass
    return _fake_db


@pytest.fixture
def funk_dict():
    funk_dict = {
        'multiline': 'echo Hello\necho world!',
        'T': 'echo RUN $1',
        'TT': 'echo CHICKEN $@',
    }
    return funk_dict


@pytest.fixture
def global_funk_dict():
    g_funk_dict = {
        'T': 'echo "GLOBAL ALIAS"',
    }
    return g_funk_dict


@pytest.fixture(params=[
    (['T', 'PROGRAM'], False),
    (['TT', 'WING'], False),
    (['multiline'], False)
], ids=['T', 'TT', 'multiline'])
def args(request):
    """Returns a named tuple of command arguments and expected results."""
    Args = collections.namedtuple('Args', ['args', 'color'])
    return Args(request.param[0], request.param[1])
