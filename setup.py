#! /usr/bin/env python


import os

from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as stream:
        return stream.read()


setup(
    name="tagterm",
    version="0.1",
    description="Remove tags from valid XHTML files.",
    long_description=read("README.md"),
    url="https://github.com/cmin764/tagterm.git",
    license="MIT",
    author='Cosmin "cmiN" Poieana',
    author_email="cmin764@gmail.com",
    packages=["tagterm"],
    scripts=["bin/tagterm"],
    package_data={"tagterm": ["etc/tagterm/*"]},
    include_package_data=True,
    install_requires=read("requirements.txt").splitlines()
)
