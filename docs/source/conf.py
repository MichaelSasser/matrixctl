# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

"""Use this module to generate the documentation with ``sphinx``."""

import os
import sys

from datetime import date
from typing import List

from pkg_resources import get_distribution


__version__: str = get_distribution("matrixctl").version

sys.path.insert(0, os.path.abspath("../"))
sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------

project: str = "MatrixCtl"
author: str = "Michael Sasser"
project_copyright: str = f"{date.today().year}, {author}"

# The full version, including alpha/beta/rc tags
version: str = __version__
release: str = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions: List[str] = [
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx_autodoc_typehints",
    "sphinxcontrib.programoutput",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.viewcode",
    "numpydoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.inheritance_diagram",
]

source_encoding: str = "utf-8"

# true: will complain about missing docstrings
nitpicky: bool = False
# true: figures, tables ,code-blocks are auto numbered if they have a caption.
numfig: bool = True


numpydoc_show_class_members: bool = False
# generate autosummary even if no references
autosummary_generate: bool = True
autosummary_imported_members: bool = True

# Add any paths that contain templates here, relative to this directory.
templates_path: List[str] = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: List[str] = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme: str = "classic"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path: List[str] = ["_static"]
