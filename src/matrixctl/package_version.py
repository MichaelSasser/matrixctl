# matrixctl
# Copyright (c) 2021-2023  Michael Sasser <Michael@MichaelSasser.org>
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
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Get the packages version.

The package's version is determined by first checking if a
``pyproject.toml``exists. If this is given, the version variable is
searched line by line in the file using a regular expression. When a
match occurs, the version is returned. If the ``pyproject.toml`` does
not exist, e.g. because the package was installed, it uses the version
stored in the package's metadata. In any case, if the version could not
be determined, it will return ``None``.

"""

from __future__ import annotations

import re
import typing as t

from contextlib import suppress
from pathlib import Path


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


# semver
VERSION_PATTERN: str = (
    r"^\s*version\s*=\s*[\"']\s*"
    r"(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>"
    r"(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?\s*[\"']\s*$"
)
# Fast approx. for simpel versions


def __from_pyproject(file: Path) -> str | None:
    """Get the version of a Python package from the pyproject.toml.

    Parameters
    ----------
    file : pythlib.Path
        The filepath to the pyproject.toml file.

    Returns
    -------
    version : str or None
        The package version, if the ``pyproject.toml`` and the variable
        ``version`` inside it exists. Otherwise, it will return ``None``.
        If the package is installed, the return value will be ``None``.

    """
    with suppress(FileNotFoundError), file.open() as fp:
        vers: t.Pattern[str] = re.compile(VERSION_PATTERN)
        for line in fp:
            version: t.Match[str] | None = vers.search(line)
            if version is not None:
                # semver
                return (
                    f"{version.group(1)}."
                    f"{version.group(2) or '0'}."
                    f"{version.group(3) or '0'}"
                    f"{f'-{version.group(4)}' if version.group(4) else ''}"
                    f"{f'+{version.group(5)}' if version.group(5) else ''}"
                )
                # Fast approx.
    return None


def __from_metadata(name: str) -> str | None:
    """Get the version of a Python package from the Metadata.

    Parameters
    ----------
    name : str
        The packages ``__name__``.

    Returns
    -------
    version : str or None
        The package version, if the package is installed and the version
        of it is stored in the packages metadata.

    """
    import importlib.metadata as importlib_metadata  # Python >= 3.8

    with suppress(importlib_metadata.PackageNotFoundError):
        return importlib_metadata.version(name).strip()
    return None


def get_version(name: str, file: str | Path) -> str | None:
    """Get the version of a Python package.

    Examples
    --------
    .. code-block:: python

       # file: __init__.py

       from .package_version import get_version

        __version__: str | None = get_version(__name__, __file__)

        # or
        __version__: str = get_version(__name__, __file__) or "Unknown"

        # Optional:
        if __version__ is None:
            raise ValueError("Could not find the version of the package.")

    .. code-block:: python

       # file: conf.py (sphinx)

       import sys

       sys.path.insert(0, os.path.abspath("../"))
       sys.path.insert(0, os.path.abspath("../.."))

       from matrixctl.package_version import get_version

       __version__: str = (
           get_version("matrixctl", Path(__file__).parent) or "Unknown"
       )

    Parameters
    ----------
    name : str
        The packages ``__name__``.
    file : str
        The ``__name__`` of ``__init__.py``

    Returns
    -------
    version : str or None
        The package version, if the package is installed and the version
        of it is stored in the packages metadata.

    """
    file_: Path = Path(file).parent.parent / "pyproject.toml"
    return __from_pyproject(file_) or __from_metadata(name)
