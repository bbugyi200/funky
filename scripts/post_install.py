"""Setuptools post install script."""

import errno
import getpass
import os
import shutil


def run():
    package_dir = os.path.dirname(os.path.realpath(__file__))
    _install_zsh_plugin(package_dir)


def _install_zsh_plugin(package_dir):
    """Copys zsh plugin to oh-my-zsh plugin dir (if oh-my-zsh is installed)."""
    zsh_custom_dirs = ['/home/{}/.oh-my-zsh/custom'.format(getpass.getuser()),
                       '/usr/share/oh-my-zsh/custom']

    ohmyzsh_dir = None
    for directory in zsh_custom_dirs:
        if os.path.isdir(directory):
            ohmyzsh_dir = directory
            break

    if ohmyzsh_dir is None:
        return

    _create_dir(ohmyzsh_dir + '/plugins/localalias')

    src = '{}/localalias/shell/localalias.sh'.format(os.path.dirname(package_dir))
    dest = '{}/plugins/localalias/{}'.format(ohmyzsh_dir, 'localalias.plugin.zsh')
    shutil.copyfile(src, dest)


def _create_dir(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            return


if __name__ == "__main__":
    run()
