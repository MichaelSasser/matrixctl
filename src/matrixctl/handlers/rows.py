"""Use this module to output events as rows."""

from __future__ import annotations

import logging
import os
import shutil
import typing as t

from rich.text import Text
from typing_extensions import Self

from matrixctl.errors import NotAnEventError
from matrixctl.handlers.api import download_media_to_buf
from matrixctl.handlers.yaml import YAML
from matrixctl.sanitizers import MessageType
from matrixctl.terminal import TerminalCellSizePx
from matrixctl.terminal import get_terminal_cell_size_in_px
from matrixctl.terminal import imgcat


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)

EventContent: t.TypeAlias = dict[str, t.Any]
Event: t.TypeAlias = dict[str, t.Any | EventContent]


class Ctx:
    """A container that keeps track of the text and post_buf."""

    def __init__(
        self, text: None | Text = None, post_buf: None | bytes = None
    ) -> None:
        self.text: Text = text or Text()
        self.post_buf: bytes = post_buf or b""

    def append(
        self, text: None | Text = None, post_buf: None | bytes = None
    ) -> None:
        """Append text or post_buf to the context."""
        if text is not None:
            self.text += text
        if post_buf is not None:
            self.post_buf += post_buf

    def __add__(self, cls: Ctx) -> Ctx:
        """Merge two contexts together, creating a new one."""
        return Ctx(
            text=self.text + cls.text, post_buf=self.post_buf + cls.post_buf
        )

    def __iadd__(self, cls: Ctx) -> Self:
        """Merge two contexts together, modifying the current one."""
        self.text += cls.text
        self.post_buf += cls.post_buf
        return self


def get_event_type_from_event(ev: Event) -> MessageType | str:
    """Get the event type from the event."""
    kind_: t.Any = ev.get("type")
    if not isinstance(kind_, str):
        err_msg: str = f"The given event data is not a valid event. {ev=}"
        logger.error(err_msg)
        raise NotAnEventError(err_msg)
    kind: MessageType | str
    try:
        kind = MessageType.from_string(kind_)
    except ValueError:
        kind = kind_
    return kind


def get_event_content_from_event(ev: Event) -> dict[str, t.Any]:
    """Get the event content from the event."""
    content: None | t.Any = ev.get("content")
    if not isinstance(content, dict):
        kind = get_event_type_from_event(ev)
        err_msg: str = (
            f"The given, with the event type {kind} is not a valid event, "
            f"as it is missing the content field. {ev=}"
        )
        logger.error(err_msg)
        raise NotAnEventError(err_msg)
    return content


def _ev_m_room_redaction(ev: Event, _: YAML) -> Ctx:
    """Create a context for a redaction event."""
    ctx: Ctx = Ctx()

    redacts = ev.get("redacts")
    ctx.append(Text("REDACTION ", "bright_black italic"))
    if redacts is not None:
        ctx.append(Text(f"{{ redacts={redacts} }}", style="bright_black"))

    return ctx


def _ev_m_room_guest_access(ev: Event, _: YAML) -> Ctx:
    """Create a context for a guest access event."""
    ctx: Ctx = Ctx()

    content: EventContent = get_event_content_from_event(ev)

    ctx.append(Text("GUEST ACCESS ", "bright_black italic"))
    ctx.append(Text(f"{{ content={content} }}", style="bright_black"))

    return ctx


def _ev_m_room_history_visibility(ev: Event, _: YAML) -> Ctx:
    """Create a context for a history visibility event."""
    ctx: Ctx = Ctx()

    content: EventContent = get_event_content_from_event(ev)

    ctx.append(Text("HISTORY VISIBILITY ", "bright_black italic"))
    ctx.append(Text(f"{{ content={content} }}", style="bright_black"))

    return ctx


def _ev_m_room_join_rules(ev: Event, _: YAML) -> Ctx:
    """Create a context for a join rules event."""
    ctx: Ctx = Ctx()

    content: EventContent = get_event_content_from_event(ev)

    ctx.append(Text("JOIN RULES ", "bright_black italic"))
    ctx.append(Text(f"{{ content={content} }}", style="bright_black"))

    return ctx


def _ev_m_room_power_levels(ev: Event, _: YAML) -> Ctx:
    """Create a context for a power levels event."""
    ctx: Ctx = Ctx()

    content: EventContent = get_event_content_from_event(ev)

    ctx.append(Text("POWER LEVELS ", "bright_black italic"))
    ctx.append(Text(f"{{ content={content} }}", style="bright_black"))

    return ctx


def _ev_m_room_encrypted(_1: Event, _2: YAML) -> Ctx:
    """Create a context for an encrypted event."""
    ctx: Ctx = Ctx()

    ctx.append(Text("MESSAGE ENCRYPTED", "bright_black italic"))

    return ctx


def _ev_m_reaction(ev: Event, _: YAML) -> Ctx:
    """Create a context for a reaction event."""
    ctx: Ctx = Ctx()

    content: EventContent = get_event_content_from_event(ev)

    relates_to = content.get("m.relates_to")

    if relates_to is not None:
        relates_to_event_id = relates_to.get("event_id")
        rel_type = relates_to.get("rel_type")

        if rel_type == "m.annotation":
            ctx.append(Text("ANNOTATION ", "bright_black italic"))
            ctx.append(Text("{ ", style="bright_black"))

            key = relates_to.get("key")

            ctx.append(
                Text(
                    "key='",
                    "bright_black",
                )
            )

            ctx.append(
                Text(
                    key,
                    "green",
                )
            )

            ctx.append(
                Text(
                    "' ",
                    "bright_black",
                )
            )

            ctx.append(
                Text(
                    f"relates_to={relates_to_event_id} rel_type={rel_type} ",
                    "bright_black",
                )
            )

            ctx.append(Text("}", style="bright_black"))

    return ctx


def _ev_m_room_message_text(ev: Event, _: YAML) -> Ctx:
    """Create a context for a text message event."""
    ctx: Ctx = Ctx()

    content: EventContent = get_event_content_from_event(ev)
    body: str = str(content.get("body"))

    mgstype: str = str(content.get("msgtype"))
    ctx.append(Text(f"{mgstype.lstrip('m.').upper()} ", "bright_black italic"))
    ctx.append(Text("{ ", style="bright_black"))

    ctx.append(Text("body='", style="bright_black"))
    ctx.append(Text(body, style="green"))
    ctx.append(Text("' ", style="bright_black"))

    relates_to = content.get("m.relates_to")
    reply_to_event_id = None
    if relates_to is not None:
        in_reply_to = relates_to.get("m.in_reply_to")
        if in_reply_to is not None:
            reply_to_event_id = in_reply_to.get("event_id")
            ctx.append(
                Text(f"replies_to={reply_to_event_id} ", "bright_black")
            )

    ctx.append(Text("}", style="bright_black"))

    return ctx


def _ev_m_room_message_image(ev: Event, yaml: YAML) -> Ctx:
    """Create a context for an image message event."""
    ctx: Ctx = Ctx()

    content: EventContent = get_event_content_from_event(ev)
    body: str = str(content.get("body"))
    url = content.get("url")

    info = content.get("info")

    ctx.append(Text("IMAGE ", "bright_black italic"))
    ctx.append(
        Text(
            f"{{ {body=}, {url=}",
            "bright_black",
        )
    )
    if info is not None:
        mimetype = info.get("mimetype")
        size = info.get("size")
        width = info.get("w")
        height = info.get("h")

        ctx.append(
            Text(
                (
                    f" mimetype={mimetype}, size={size},"
                    f" width={width}, height={height}"
                ),
                "bright_black",
            )
        )
    ctx.append(Text(" }", "bright_black"))

    if (
        isinstance(url, str)
        and url.startswith("mxc://")
        and yaml.get("ui", "image", "enabled")
    ):
        terminal_cell_size: TerminalCellSizePx | None = (
            get_terminal_cell_size_in_px()
        )

        if terminal_cell_size is not None:
            terminal_size: os.terminal_size = shutil.get_terminal_size(
                (80, 20)
            )
            # Number of lines times their height in px
            terminal_height: int = (
                terminal_size.lines * terminal_cell_size.height
            )
            terminal_width: int = (
                terminal_size.columns * terminal_cell_size.width
            )

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
            token=yaml.get("server", "api", "token"),
            domain=yaml.get("server", "api", "domain"),
            media_id=url,
        )
        buf = imgcat(
            buf_image,
            height=f"{scaled_height}px",
            preserve_aspect_ratio=True,
        )
        ctx.append(post_buf=buf)

    return ctx


def _ev_m_room_message_file(ev: Event, _: YAML) -> Ctx:
    """Create a context for a file message event."""
    ctx: Ctx = Ctx()

    content: EventContent = get_event_content_from_event(ev)

    body: str = str(content.get("body"))
    url = content.get("url")

    info = content.get("info")

    ctx.append(Text("FILE ", "bright_black italic"))
    ctx.append(
        Text(
            f"{{ {body=}, {url=}",
            "bright_black",
        )
    )
    if info is not None:
        mimetype = info.get("mimetype")
        size = info.get("size")

        ctx.append(
            Text(
                (f" mimetype={mimetype}, size={size},"),
                "bright_black",
            )
        )
    ctx.append(Text(" }", "bright_black"))

    return ctx


def _ev_m_room_message(ev: Event, yaml: YAML) -> Ctx:
    """Create a context for a message event."""
    ctx: Ctx = Ctx()

    content: EventContent = get_event_content_from_event(ev)

    mgstype: str = str(content.get("msgtype"))

    match mgstype:
        case "m.text" | "m.notice":
            ctx = _ev_m_room_message_text(ev, yaml)
        case "m.image":
            ctx = _ev_m_room_message_image(ev, yaml)
        case "m.file":
            ctx = _ev_m_room_message_file(ev, yaml)
        case _:
            ctx = Ctx(Text(f"Unknown Message Type '{mgstype}"))

    return ctx


def _ev_m_room_member(ev: Event, _: YAML) -> Ctx:
    """Create a context for a member event."""
    ctx: Ctx = Ctx()

    content: EventContent = get_event_content_from_event(ev)
    avatar_url: str | None = content.get("avatar_url")
    displayname: str | None = content.get("displayname")
    membership: str | None = content.get("membership")

    ctx.append(Text("MEMBERSHIP ", "bright_black italic"))
    ctx.append(
        Text(
            f"{{ {membership=}, {displayname=}, {avatar_url=} }}",
            "bright_black",
        )
    )

    return ctx


def to_row_context(ev: dict[str, t.Any], yaml: YAML) -> Ctx:
    """Create an event context from a message type and it's content."""
    ctx: Ctx

    kind: MessageType | str = get_event_type_from_event(ev)
    match kind:
        case MessageType.M_ROOM_REDACTION:
            ctx = _ev_m_room_redaction(ev, yaml)
        case MessageType.M_ROOM_GUEST_ACCESS:
            ctx = _ev_m_room_guest_access(ev, yaml)
        case MessageType.M_ROOM_HISTORY_VISIBILITY:
            ctx = _ev_m_room_history_visibility(ev, yaml)
        case MessageType.M_ROOM_JOIN_RULES:
            ctx = _ev_m_room_join_rules(ev, yaml)
        case MessageType.M_ROOM_POWER_LEVELS:
            ctx = _ev_m_room_power_levels(ev, yaml)
        case MessageType.M_ROOM_ENCRYPTED:
            ctx = _ev_m_room_encrypted(ev, yaml)
        case MessageType.M_REACTION:
            ctx = _ev_m_reaction(ev, yaml)
        case MessageType.M_ROOM_MESSAGE:
            ctx = _ev_m_room_message(ev, yaml)
        case MessageType.M_ROOM_MEMBER:
            ctx = _ev_m_room_member(ev, yaml)
        case _:
            ctx = Ctx(Text("Unknown Message Type"))
    return ctx
