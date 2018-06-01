#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from setuptools.command.install import install

from scripts import post_install


class PostInstallCommand(install):
    """Post-installation for install mode."""
    def run(self):
        post_install.run()
        install.run(self)


with open('README.rst') as readme_file:
    readme = readme_file.read()


setup(
    author="Bryan M Bugyi",
    author_email='bryanbugyi34@gmail.com',
    install_requires=['pygments'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    cmdclass={'install': PostInstallCommand},
    description="A light-weight shell wrapper that allows you to create per-directoy command aliases.",
    entry_points={
        'console_scripts': [
            'localalias = localalias.app:main',
            'la = localalias.app:main'
        ]
    },
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='localalias',
    name='localalias',
    packages=find_packages(include=['localalias', 'localalias.utils']),
    test_suite='tests',
    tests_require=['pytest'],
    url='https://github.com/bbugyi200/localalias',
    version='2.0.2',
    zip_safe=False,
)
