"""Setuptools post install script."""

import errno
import getpass
import os
import shutil


def run():
    _install_zsh_plugin()


def _install_zsh_plugin():
    """Copys zsh plugin to oh-my-zsh plugin dir (if oh-my-zsh) is installed."""
    zsh_custom_dirs = ['/home/{}/.oh-my-zsh/custom'.format(getpass.getuser()),
                       '/usr/share/oh-my-zsh/custom']

    ohmyzsh_dir = None
    for directory in zsh_custom_dirs:
        if os.path.isdir(directory):
            ohmyzsh_dir = directory
            break

    if ohmyzsh_dir is None:
        return

    try:
        os.makedirs(ohmyzsh_dir + '/plugins/localalias')
    except OSError as e:
        if e.errno != errno.EEXIST:
            return

    src = '{}/zsh/localalias.zsh'.format(os.path.dirname(os.path.realpath(__file__)))
    dest = '{}/plugins/localalias/{}'.format(ohmyzsh_dir, 'localalias.plugin.zsh')
    shutil.copyfile(src, dest)


if __name__ == "__main__":
    run()
