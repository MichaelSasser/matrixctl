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

"""Use the functions of this module as printing helpers."""

from __future__ import annotations

import os
import typing as t

from base64 import b64encode
from datetime import datetime
from datetime import timezone


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


BIN_ESC: bytes[str] = b"\033"
BIN_NL: bytes[str] = b"\n"
BIN_BEL: bytes[str] = b"\a"


# TODO: Check if used and for what; type?; docs.
def human_readable_bool(b: t.Any) -> str:
    """Use this helper function to get a "yes" or "no" string from a "bool".

    Parameters
    ----------
    b : any
        The value to "convert".

    Returns
    -------
    answer : str
        ``"Yes"`` if expression is ``True``, or
        ``"False"`` if expression is ``False``.

    """
    if isinstance(b, str):
        b = int(b)

    if isinstance(b, int):
        b = bool(b)

    return "Yes" if b else "No"


def timestamp_to_dt(ts: str, sep: str = " ") -> str:
    """Convert a timestamp (in ms) to a datetime string.

    Parameters
    ----------
    ts : str
        The value to "convert".
    sep : str
        The separator between the date and the time.

    Returns
    -------
    dt : str
        A datetime string (e.g. 2021-08-21 04:55:55)

    """
    return (
        datetime.fromtimestamp(int(ts) // 1000.0, tz=timezone.utc)
        .strftime("%Y-%m-%d %H:%M:%S")
        .replace(" ", sep)
    )


def _generate_osc_cs(
    command: int, arguments: dict[str, str], *, term_is_tmux: bool = False
) -> bytes[str]:
    """Get an operating system command (OSC) control sequence.

    Parameters
    ----------
     term_is_tmux : bool
        `True`, if the terminal is tmux, `False` if not.

    Returns
    -------
    bytes : bytes
        Contains the OSC control sequence.

    """
    buf: bytes[str] = BIN_ESC
    if term_is_tmux:
        buf += b"Ptmux;"
        buf += BIN_ESC
        buf += BIN_ESC
    buf += b"]"

    buf += str(command).encode()

    for k, v in arguments.items():
        buf += b";"
        buf += k.encode()
        buf += b"="
        buf += v.encode()
    return buf


def _generate_st(*, term_is_tmux: bool = False) -> bytes[str]:
    """Generate an ST space character.

    Parameters
    ----------
     term_is_tmux : bool
        `True`, if the terminal is tmux, `False` if not.

    Returns
    -------
    bytes : bytes
        Contains the ST space character.

    """

    buf: bytes[str] = BIN_BEL
    if term_is_tmux:
        buf += BIN_ESC
        buf += b"\\"

    buf += BIN_NL
    return buf


def imgcat(
    data: bytes,
    width: int | str = "auto",
    height: int | str = "auto",
    *,
    preserve_aspect_ratio: bool = False,
    inline: bool = True,
) -> bytes[str]:
    """Output an image on the terminal.

    Parameters
    ----------
    data : bytes
        A buffer containing the raw image data.
    width : int or str
        The width are given as a number followed by a unit, or the
        word "auto".

        - `N`: N character cells.
        - `"Npx"`: N pixels.
        - `"N%"`: N percent of the session's width or height.
        - `"auto"`: The image's inherent size will be used to determine an
          appropriate dimension.
    height : int or str
        The height are given as a number followed by a unit, or the
        word "auto".

        - `N`: N character cells.
        - `"Npx"`: N pixels.
        - `"N%"`: N percent of the session's width or height.
        - `"auto"`: The image's inherent size will be used to determine an
          appropriate dimension.
    preserve_aspect_ratio : bool
        If set to `False`, then the image's inherent aspect ratio will not be
        respected; otherwise, it will fill the specified width and height
        as much as possible without stretching. Defaults to `True`.
    inline : bool
        If set to `True`, the file will be displayed inline. Otherwise,
        it will be downloaded with no visual representation in the terminal
        session. Defaults to `True`.

    Returns
    -------
    bytes : bytes
        A buffer containing the entire escape sequence, which can be written
        to the terminal as follows.

        .. code-block:: python
           from sys import stdout


           buf = imgcat(...)

           stdout.buffer.write(buf)
           stdout.flush()

    Notes
    -----
    The documentation for this function mostly comes from:
    - `Escape Codes <https://iterm2.com/documentation-escape-codes.html>`_
    - `Terminal Images <https://iterm2.com/documentation-images.html>`_

    """
    term_is_tmux: bool = os.environ["TERM"].startswith("screen")

    buf: bytes[str] = _generate_osc_cs(
        1337,
        {
            "File": "",
            "size": str(len(data)),
            "inline": str(int(inline)),
            "preserveAspectRatio": str(int(preserve_aspect_ratio)),
            "width": str(width),
            "height": str(height),
        },
        term_is_tmux=term_is_tmux,
    )

    buf += b":"
    buf += b64encode(data)

    # ST
    buf += _generate_st(term_is_tmux=term_is_tmux)

    return buf


# vim: set ft=python :
