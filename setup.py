"""Supermercado."""

import os
from codecs import open as codecs_open

from setuptools import find_packages, setup

# Get the long description from the relevant file
with codecs_open("README.md", encoding="utf-8") as f:
    long_description = f.read()


def read(fname):
    """Filename."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="supermercado",
    version="0.2.0",
    description=u"Supercharged mercantile",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[],
    keywords="",
    author=u"Damon Burgett",
    author_email="damon@mapbox.com",
    url="https://github.com/mapbox/supermercado",
    license="MIT",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=read("requirements.txt").splitlines(),
    extras_require={"test": ["pytest", "pytest-cov", "codecov"]},
    entry_points="""
      [console_scripts]
      supermercado=supermercado.scripts.cli:cli
      """,
)
