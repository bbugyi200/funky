from collections import namedtuple
import os

import pytest

from scripts import post_install


def test_copy_sh_ext__ENVVAR_DEFINED():
    old_data_dir = os.environ.get('XDG_DATA_HOME', None)
    os.environ['XDG_DATA_HOME'] = '/tmp'

    Install = namedtuple('Install', ['root'])
    install = Install(None)
    post_install._copy_sh_ext(install)

    assert os.path.exists('/tmp/funky/funky.sh')
    os.system('rm -rf /tmp/funky')

    if old_data_dir:
        os.environ['XDG_DATA_HOME'] = old_data_dir
    else:
        del os.environ['XDG_DATA_HOME']


def test_copy_sh_ext__ENVVAR_NOT_DEFINED():
    old_data_dir = os.environ.get('XDG_DATA_HOME', None)

    if 'XDG_DATA_HOME' in os.environ:
        del os.environ['XDG_DATA_HOME']

    Install = namedtuple('Install', ['root'])
    install = Install('/tmp/')
    post_install._copy_sh_ext(install)

    os.path.exists(f"/tmp/home/{os.environ['USER']}/.local/share/funky/funky.sh")
    os.system('rm -rf /tmp/home')

    if old_data_dir:
        os.environ['XDG_DATA_HOME'] = old_data_dir
