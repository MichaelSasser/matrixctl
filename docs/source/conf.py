# matrixctl
# Copyright (c) 2020-2023  Michael Sasser <Michael@MichaelSasser.org>
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

import sys

from datetime import datetime
from datetime import timezone
from pathlib import Path


sys.path.insert(0, str(Path("../").resolve()))
sys.path.insert(0, str(Path("../..").resolve()))
sys.path.insert(0, str((Path("../") / "src").resolve()))
sys.path.insert(0, str((Path("../..") / "src").resolve()))

from matrixctl.package_version import get_version  # skipcq: FLK-E402


__version__: str = get_version("matrixctl", Path(__file__).parent) or "Unknown"

# -- Project information -----------------------------------------------------

project: str = "MatrixCtl"
author: str = "Michael Sasser"
project_copyright: str = (
    f"{datetime.now(tz=timezone.utc).date().year}, {author}"
)

# The full version, including alpha/beta/rc tags
version: str = __version__
release: str = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions: list[str] = [
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx_autodoc_typehints",
    "sphinx_rtd_theme",
    "sphinxcontrib.programoutput",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.viewcode",
    "numpydoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.inheritance_diagram",
    "myst_parser",
]

source_suffix: dict[str, str] = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

suppress_warnings: list[str] = ["autosectionlabel.*"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
intersphinx_timeout = 10

source_encoding: str = "utf-8"

# true: will complain about missing docstrings
nitpicky: bool = False
# true: figures, tables ,code-blocks are auto numbered if they have a caption.
numfig: bool = True

# This will not work for now and will generate a lot of warnings since
# gitpython has a circular import somewhere when this option is enabled
set_type_checking_flag = False  # sphinx-autodoc-typehints: set TYPE_CHECKING

numpydoc_show_class_members: bool = False

# Whether to create cross-references for the parameter types in the
# Parameters, Other Parameters, Returns and Yields sections of the docstring.
# False by default.
numpydoc_xref_param_type: bool = True

# Report warnings for all validation checks
# TODO: numpydoc_validation_checks = {"all"}

# generate autosummary even if no references
autosummary_generate: bool = True
autosummary_imported_members: bool = True

# Add any paths that contain templates here, relative to this directory.
templates_path: list[str] = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: list[str] = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme: str = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path: list[str] = ["_static"]
