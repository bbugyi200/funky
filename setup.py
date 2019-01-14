#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

import funky
from scripts import post_install


class PostInstallCommand(install):
    """Post-installation for install mode."""
    def run(self):
        post_install.run(self)
        install.run(self)


class PostDevelopCommand(develop):
    """Post-installation for develop mode."""
    def run(self):
        post_install.run()
        develop.run(self)


with open('README.md') as readme_file:
    readme = readme_file.read()


setup(
    author="Bryan M Bugyi",
    author_email='bryanbugyi34@gmail.com',
    install_requires=['pygments'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    cmdclass={
        'install': PostInstallCommand,
        'develop': PostDevelopCommand,
    },
    description=funky.__doc__,
    entry_points={
        'console_scripts': [
            'funky = funky.app:main',
        ]
    },
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='funky',
    name='pyfunky',
    packages=find_packages(),
    test_suite='tests',
    tests_require=['pytest'],
    url='https://github.com/bbugyi200/funky',
    version='3.3.0',
    zip_safe=False,
)
