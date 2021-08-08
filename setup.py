# -*- coding: utf-8 -*-

"""The setup script."""

from pathlib import Path
from typing import Iterator, List

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

import funky
from scripts import post_install


class PostInstallCommand(install):
    """Post-installation for install mode."""

    def run(self):
        post_install.run(self)
        super().run()


class PostDevelopCommand(develop):
    """Post-installation for develop mode."""

    def run(self):
        post_install.run(self)
        super().run()


def long_description() -> str:
    return Path("README.md").read_text()


def install_requires() -> List[str]:
    return list(_requires("requirements.txt"))


def tests_require() -> List[str]:
    return list(_requires("dev-requirements.txt"))


def _requires(reqtxt_basename: str) -> Iterator[str]:
    reqtxt = Path(__file__).parent / reqtxt_basename
    reqs = reqtxt.read_text().split("\n")
    for req in reqs:
        if not req or req.lstrip().startswith(("#", "-")):
            continue
        yield req


setup(
    author="Bryan M Bugyi",
    author_email="bryanbugyi34@gmail.com",
    install_requires=install_requires(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    cmdclass={
        "install": PostInstallCommand,
        "develop": PostDevelopCommand,
    },
    description=funky.__doc__,
    entry_points={
        "console_scripts": [
            "funky = funky.app:main",
        ]
    },
    license="MIT license",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="funky",
    name="pyfunky",
    packages=find_packages(),
    test_suite="tests",
    tests_require=tests_require(),
    url="https://github.com/bbugyi200/funky",
    version="3.4.1",
    zip_safe=False,
)
