import collections
import json
import os
import shutil
import tempfile
import unittest.mock as mock

import pytest

from localalias import commands


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
    """Setup/teardown a global alias database"""
    _fake_db = _fake_db_factory(global_filename, global_alias_dict)
    yield from _fake_db()


@pytest.fixture
def global_filename():
    """Returns a fake global database path so the production global db is not overwritten."""
    return "/tmp/.globalalias"


@pytest.fixture
def fake_db():
    """Setup/teardown a local alias database"""
    _fake_db = _fake_db_factory(commands.Command.LOCALALIAS_DB_FILENAME, alias_dict)
    yield from _fake_db()


def _fake_db_factory(DB_FILENAME, alias_dict_builder):
    """Builds a generator fixture for creating a fake database."""
    def _fake_db():
        my_alias_dict = alias_dict_builder()
        with open(DB_FILENAME, 'w') as f:
            json.dump(my_alias_dict, f)
        yield my_alias_dict
        try:
            os.remove(DB_FILENAME)
        except FileNotFoundError:
            pass
    return _fake_db


@pytest.fixture
def alias_dict():
    alias_dict = {
        'multiline': 'echo Hello\necho world!',
        'T': 'echo RUN $1',
        'TT': 'echo CHICKEN $@',
    }
    return alias_dict


@pytest.fixture
def global_alias_dict():
    g_alias_dict = {
        'T': 'echo "GLOBAL ALIAS"',
    }
    return g_alias_dict


@pytest.fixture(params=[
    (['T', 'PROGRAM'], False),
    (['TT', 'WING'], False),
    (['multiline'], False)
], ids=['T', 'TT', 'multiline'])
def args(request):
    """Returns a named tuple of command arguments and expected results."""
    Args = collections.namedtuple('Args', ['args', 'color'])
    return Args(request.param[0], request.param[1])
