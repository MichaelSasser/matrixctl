"""Use this module to output events as rows."""

from __future__ import annotations

import logging
import typing as t

from rich.text import Text

from matrixctl.errors import NotAnEventError
from matrixctl.handlers.api import download_media_to_buf
from matrixctl.handlers.yaml import YAML
from matrixctl.print_helpers import imgcat
from matrixctl.sanitizers import MessageType


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)

event_content: t.TypeAlias = dict[str, t.Any]
event: t.TypeAlias = dict[str, t.Any | event_content]


class Ctx:
    def __init__(
        self, text: None | Text = None, post_buf: None | bytes = None
    ) -> None:
        self.text: Text = text or Text()
        self.post_buf: bytes = post_buf or b""

    def append(
        self, text: None | Text = None, post_buf: None | bytes = None
    ) -> None:
        if text is not None:
            self.text += text
        if post_buf is not None:
            self.post_buf += post_buf

    def __add__(self, cls: Ctx) -> Ctx:
        return Ctx(
            text=self.text + cls.text, post_buf=self.post_buf + cls.post_buf
        )

    def __iadd__(self, cls: Ctx) -> Ctx:
        self.text += cls.text
        self.post_buf += cls.post_buf
        return self


def get_event_type_from_event(ev: event) -> MessageType | str:
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


def get_event_content_from_event(ev: event) -> dict[str, t.Any]:
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


def _ev_m_room_redaction(ev: event, _: YAML) -> Ctx:
    ctx: Ctx = Ctx()

    redacts = ev.get("redacts")
    ctx.append(Text("REDACTION ", "bright_black italic"))
    if redacts is not None:
        ctx.append(f"{{ redacts={redacts} }}", style="bright_black")

    return ctx


def _ev_m_room_guest_access(ev: event, _: YAML) -> Ctx:
    ctx: Ctx = Ctx()

    content: event_content = get_event_content_from_event(ev)

    ctx.append(Text("GUEST ACCESS ", "bright_black italic"))
    ctx.append(Text(f"{{ content={content} }}", style="bright_black"))

    return ctx


def _ev_m_room_history_visibility(ev: event, _: YAML) -> Ctx:
    ctx: Ctx = Ctx()

    content: event_content = get_event_content_from_event(ev)

    ctx.append(Text("HISTORY VISIBILITY ", "bright_black italic"))
    ctx.append(Text(f"{{ content={content} }}", style="bright_black"))

    return ctx


def _ev_m_room_join_rules(ev: event, _: YAML) -> Ctx:
    ctx: Ctx = Ctx()

    content: event_content = get_event_content_from_event(ev)

    ctx.append(Text("JOIN RULES ", "bright_black italic"))
    ctx.append(Text(f"{{ content={content} }}", style="bright_black"))

    return ctx


def _ev_m_room_power_levels(ev: event, _: YAML) -> Ctx:
    ctx: Ctx = Ctx()

    content: event_content = get_event_content_from_event(ev)

    ctx.append(Text("POWER LEVELS ", "bright_black italic"))
    ctx.append(Text(f"{{ content={content} }}", style="bright_black"))

    return ctx


def _ev_m_room_encrypted(ev: event, _: YAML) -> Ctx:
    ctx: Ctx = Ctx()

    ctx.append(Text("MESSAGE ENCRYPTED", "bright_black italic"))

    return ctx


def _ev_m_reaction(ev: event, _: YAML) -> Ctx:
    ctx: Ctx = Ctx()

    content: event_content = get_event_content_from_event(ev)

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


def _ev_m_room_message_text(ev: event, _: YAML) -> Ctx:
    ctx: Ctx = Ctx()

    content: event_content = get_event_content_from_event(ev)
    body: str = str(content.get("body"))

    mgstype: str = str(content.get("msgtype"))
    ctx.append(
        Text(f"{mgstype.lstrip('m.').upper() } ", "bright_black italic")
    )
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


def _ev_m_room_message_image(ev: event, yaml: YAML) -> Ctx:
    ctx: Ctx = Ctx()

    content: event_content = get_event_content_from_event(ev)
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

    if isinstance(url, str):
        # Test: This should later follow the entry
        buf_image = download_media_to_buf(
            token=yaml.get("server", "api", "token"),
            domain=yaml.get("server", "api", "domain"),
            media_id=url,
        )
        buf = imgcat(buf_image, width="90%", preserve_aspect_ratio=True)
        ctx.append(post_buf=buf)

    return ctx


def _ev_m_room_message_file(ev: event, _: YAML) -> Ctx:
    ctx: Ctx = Ctx()

    content: event_content = get_event_content_from_event(ev)

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


def _ev_m_room_message(ev: event, yaml: YAML) -> Ctx:
    ctx: Ctx = Ctx()

    content: event_content = get_event_content_from_event(ev)

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


def _ev_m_room_member(ev: event, _: YAML) -> Ctx:
    ctx: Ctx = Ctx()

    content: event_content = get_event_content_from_event(ev)
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
