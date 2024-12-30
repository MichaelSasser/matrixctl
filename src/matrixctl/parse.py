"""Use the functions to parse certain srtings."""

from __future__ import annotations

import logging
import typing as t

from matrixctl.errors import ParserError


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


ERR_MSG_INVALID_MXC_URI = (
    "The given string is not a valid matrix media URI. A valid matrix media "
    "URI starts with 'mxc://'. For example: 'mxc://homeserver/media_id'."
    "The URI given was: "
)


class Mxc(t.NamedTuple):
    """Use this named tuple to store the server and media id of a mxc uri."""

    homeserver: str
    media_id: str


def parse_mxc_uri(uri: str) -> Mxc:
    """Parse a MXC into a tuple of homeserver and media ID.

    Arguments
    ---------
    uri : str
        A URI to parse

    Returns
    -------
    Mxc : matrixctl.parse.Mxc
        A `NamedTuple` containing the `homeserver` and `media_id`.

    Raises
    ------
    matrix.errors.ParserError
        If the `uri` cannot be split.

    """
    try:
        if not uri.startswith("mxc://"):
            err_msg = (
                f"{ERR_MSG_INVALID_MXC_URI} {uri}. "
                "Please make sure the URI starts with 'mxc://'."
            )
            logger.error(err_msg)
            raise ParserError(err_msg)
        mxc_parts = uri.removeprefix("mxc://").split("/")

    except ValueError:
        err_msg = f"{ERR_MSG_INVALID_MXC_URI} {uri}."
        logger.exception(err_msg)
        raise ParserError(err_msg) from ValueError

    if len(mxc_parts) != 2:  # noqa: PLR2004
        err_msg = (
            f"{ERR_MSG_INVALID_MXC_URI} {uri}. "
            "Please make sure the URI contains both the homeserver and "
            "the media ID part separated by a '/'."
        )
        logger.error(err_msg)
        raise ParserError(err_msg)

    homeserver, media_id = mxc_parts

    return Mxc(homeserver=homeserver, media_id=media_id)
