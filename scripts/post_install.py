"""Setuptools post install script."""

import errno
import getpass
import os

_package_dir = os.path.dirname(os.path.realpath(__file__))
_user = getpass.getuser()


def run():
    _install_omz_plugin()


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

    src = '{}/localalias/shell/localalias.sh'.format(os.path.dirname(_package_dir))
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
