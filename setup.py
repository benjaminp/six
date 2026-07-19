from __future__ import with_statement

# Setuptools is used for packaging. distutils (deprecated in Python 3.10,
# removed in 3.12) is no longer used as a fallback.
from setuptools import setup

import six

six_classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

with open("README.rst", "r") as fp:
    six_long_description = fp.read()

setup(name="six",
      version=six.__version__,
      author="Benjamin Peterson",
      author_email="benjamin@python.org",
      url="https://github.com/benjaminp/six",
      tests_require=["pytest"],
      py_modules=["six"],
      description="Python 2 and 3 compatibility utilities",
      long_description=six_long_description,
      license="MIT",
      classifiers=six_classifiers,
      python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*",
      )
