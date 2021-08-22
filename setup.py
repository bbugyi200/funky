from pathlib import Path
from typing import Iterator, List

from setuptools import find_packages, setup


DESCRIPTION = (
    "Funky takes shell functions to the next level by making them easier to"
    " define, more flexible, and more interactive."
)


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
    python_requires=">=3.7",
    install_requires=install_requires(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description=DESCRIPTION,
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
    package_data={"scripts.shell": ["*.sh"]},
    packages=find_packages(),
    test_suite="tests",
    tests_require=tests_require(),
    url="https://github.com/bbugyi200/funky",
    version="3.5.4",
    zip_safe=False,
)
