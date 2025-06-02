"""Use the functions of this module as printing helpers."""

from __future__ import annotations

import logging
import os
import shutil
import typing as t

from datetime import datetime
from datetime import timezone
from functools import lru_cache

from matrixctl.errors import ParserError
from matrixctl.handlers.api import download_media_to_buf
from matrixctl.handlers.yaml import YAML
from matrixctl.sanitizers import sanitize_mxc
from matrixctl.terminal import TerminalCellSizePx
from matrixctl.terminal import get_terminal_cell_size_in_px
from matrixctl.terminal import imgcat


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


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


@lru_cache(128)
def render_image_from_mxc(
    uri: t.Any | None, width: int, height: int, yaml: YAML
) -> bytes | None:
    """Render an image from a mxc:// URI in the terminal."""
    if not yaml.get("ui", "image", "enabled"):
        return None
    uri_sanitized: str | t.Literal[False] | None = sanitize_mxc(uri)
    if not uri_sanitized:
        error_msg: str = "The given URI is not a valid mxc:// URI."
        raise ParserError(error_msg)

    terminal_cell_size: TerminalCellSizePx | None = (
        get_terminal_cell_size_in_px()
    )

    if terminal_cell_size is not None:
        terminal_size: os.terminal_size = shutil.get_terminal_size((80, 20))
        # Number of lines times their height in px
        terminal_height: int = terminal_size.lines * terminal_cell_size.height
        terminal_width: int = terminal_size.columns * terminal_cell_size.width

        user_scale_factor: float = yaml.get("ui", "image", "scale_factor")
        user_image_max_heigt: float = yaml.get(
            "ui", "image", "max_height_of_terminal"
        )

        image_max_height: float = 1.0 / user_image_max_heigt

        user_height: float = height * user_scale_factor
        user_width: float = width * user_scale_factor

        scale_factor_height: float = 1.0
        scale_factor_width: float = 1.0
        if (user_height) > (terminal_height / image_max_height):
            # Scale down height
            scale_factor_height = user_height / (
                terminal_height / image_max_height
            )
        if (user_width) > terminal_width:
            # Scale down width
            scale_factor_width = user_width / terminal_width
        scale_factor: float = max(scale_factor_height, scale_factor_width)
        logger.debug("Scale factor. scale_factor=%f", scale_factor)

        scaled_height: int = int(user_height / scale_factor)

    # Test: This should later follow the entry
    buf_image = download_media_to_buf(
        token=yaml.get_api_token(),
        domain=yaml.get("server", "api", "domain"),
        media_id=uri_sanitized,
    )
    return imgcat(
        buf_image,
        height=f"{scaled_height}px",
        preserve_aspect_ratio=True,
    )


# vim: set ft=python :
