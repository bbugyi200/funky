"""Setuptools post install script."""

import errno
import getpass
import os
import shutil

from localalias.utils import xdg

_config_dir = xdg.getdir('config')
_this_dir = os.path.dirname(os.path.realpath(__file__))
_user = getpass.getuser()


def run():
    _copy_shell_ext()
    _install_omz_plugin()


def _copy_shell_ext():
    src = '{}/shell/localalias.sh'.format(_this_dir)
    dest = '{}/localalias.sh'.format(_config_dir)
    shutil.copyfile(src, dest)


def _install_omz_plugin():
    """Install oh-my-zsh Plugin

    Creates symlink from localalias shell extension zsh plugin in oh-my-zsh plugin dir
    (if oh-my-zsh is installed).
    """
    zsh_custom_dirs = ['/home/{}/.oh-my-zsh/custom'.format(_user),
                       '/usr/share/oh-my-zsh/custom']

    ohmyzsh_dir = None
    for directory in zsh_custom_dirs:
        if os.path.isdir(directory):
            ohmyzsh_dir = directory
            break

    if ohmyzsh_dir is None:
        return

    _create_dir(ohmyzsh_dir + '/plugins/localalias')

    src = '{}/localalias.sh'.format(_config_dir)
    dest = '{}/plugins/localalias/{}'.format(ohmyzsh_dir, 'localalias.plugin.zsh')

    try:
        os.unlink(dest)
    except FileNotFoundError as e:
        pass

    os.symlink(src, dest)


def _create_dir(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            return


if __name__ == "__main__":
    run()
