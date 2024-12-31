"""Use the functions of this module as printing helpers."""

from __future__ import annotations

import typing as t

from datetime import datetime
from datetime import timezone


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


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


# vim: set ft=python :
