"""Use the functions of this module as printing helpers."""

from __future__ import annotations

import logging
import os
import sys
import termios
import tty
import typing as t

from base64 import b64encode


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


BIN_ESC: bytes = b"\033"
BIN_NL: bytes = b"\n"
BIN_BEL: bytes = b"\a"


class TerminalCellSizePx(t.NamedTuple):
    """A named tuple to store the terminal cell size in pixels.

    Attributes
    ----------
    width : int
        The width of the terminal cell in pixels.
    height : int
        The height of the terminal cell in pixels.

    """

    width: int
    height: int


def _generate_osc_cs(
    command: int, arguments: dict[str, str], *, term_is_tmux: bool = False
) -> bytes:
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
    buf: bytes = BIN_ESC
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


def _generate_st(*, term_is_tmux: bool = False) -> bytes:
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

    buf: bytes = BIN_BEL
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
) -> bytes:
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

        .. code-block::python
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

    buf: bytes = _generate_osc_cs(
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


def get_terminal_cell_size_in_px() -> TerminalCellSizePx | None:
    """Get the terminal cell size in pixels.

    Returns
    -------
    terminal_size : matrixctl.print_helpers.TerminalCellSizePx or None
        A 2-tuple containing the width and height of the terminal cell in
        pixels.

    """
    # Save the current terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        # Set the terminal to raw mode to capture the response
        tty.setraw(fd)

        buf: bytes = BIN_ESC
        buf += b"[16t"
        buf += BIN_ESC

        sys.stdout.buffer.write(buf)
        sys.stdout.flush()

        # Read the response from the terminal
        response = ""
        while True:
            ch: str = sys.stdin.read(1)
            response += ch
            if ch == "t":
                break

        # Parse the response
        parts: list[str] = response.split(";")
        height: int = int(parts[1])
        width: int = int(parts[2][:-1])

        return TerminalCellSizePx(width=width, height=height)
    except Exception:
        logger.exception(
            "Unable to determine terminal cell size in pixels. "
            "Possibly unsupported terminal."
        )
        return None
    finally:
        # Restore the terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


# vim: set ft=python :
