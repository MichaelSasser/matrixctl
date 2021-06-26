# matrixctl
# Copyright (c) 2020  Michael Sasser <Michael@MichaelSasser.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Use this module to generate the documentation with ``sphinx``."""

# Configuration file for the Sphinx documentation builder.
# !! This file needs to be compatible with Python 3.8 !!

from __future__ import annotations

import os
import sys

from datetime import date
from pathlib import Path
from typing import List

# pylint: disable=W0611
import sphinx_rtd_theme  # noqa: F401

from single_source import get_version


__version__: str = (
    get_version(__name__, Path(__file__).parent.parent) or "Unknown"
)

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
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.inheritance_diagram",
    "sphinx_rtd_theme",
]

suppress_warnings: List[str] = ["autosectionlabel.*"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    # "numpy": ("https://www.numpy.org/devdocs", None),
    # "scipy": ("https://scipy.github.io/devdocs", None),
    # "matplotlib": ("https://matplotlib.org", None),
}
intersphinx_timeout = 10

# numpydoc_xref_aliases = {
#     'LeaveOneOut': 'sklearn.model_selection.LeaveOneOut',
# }

source_encoding: str = "utf-8"

# true: will complain about missing docstrings
nitpicky: bool = False
# true: figures, tables ,code-blocks are auto numbered if they have a caption.
numfig: bool = True


numpydoc_show_class_members: bool = False

# Whether to create cross-references for the parameter types in the
# Parameters, Other Parameters, Returns and Yields sections of the docstring.
# False by default.
numpydoc_xref_param_type: bool = True

# Report warnings for all validation checks
numpydoc_validation_checks = {"all"}

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
html_theme: str = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path: List[str] = ["_static"]
