"""Packaging must not pick up a previously imported copy of six."""
import os
import runpy
import sys
import types

import six


def test_setup_uses_source_version(monkeypatch):
    metadata = {}
    setuptools = types.ModuleType("setuptools")
    setuptools.setup = lambda **kwargs: metadata.update(kwargs)
    previously_imported = types.ModuleType("six")
    previously_imported.__version__ = "0.0.0"
    monkeypatch.setitem(sys.modules, "setuptools", setuptools)
    monkeypatch.setitem(sys.modules, "six", previously_imported)
    monkeypatch.chdir(os.path.dirname(os.path.abspath(__file__)))

    runpy.run_path("setup.py", run_name="__main__")

    assert metadata["version"] == six.__version__
