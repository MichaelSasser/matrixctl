"""Custom argparse action classes."""

from __future__ import annotations

import typing as t

from argparse import Action
from argparse import ArgumentParser
from datetime import datetime
from datetime import timezone
from datetime import tzinfo
from enum import Enum
from functools import partial

import dateparser

from dateutil.tz import tzlocal


# https://docs.python.org/3/library/argparse.html#action-classes
class ArgparseActionEnum(Action):
    """Custom argparse action for Enums."""

    def __init__(  # type: ignore[no-untyped-def]
        self,
        choices: t.Sequence[str] | None = None,
        type: t.Any | None = None,  # noqa: A002
        **kwargs,  # noqa: ANN003
    ) -> None:
        enum: t.Any | None = type
        if enum is None:
            err_msg = "The enum must be provided as argument 'type'."
            raise TypeError(err_msg)
        if not issubclass(enum, Enum):
            err_msg = f"The argument type must be an Enum. The type was {enum}"
            raise TypeError(err_msg)

        self._enum = enum

        choices = choices or tuple(enum_type.value for enum_type in self._enum)

        super().__init__(choices=choices, **kwargs)

    def __call__(  # noqa: D102
        self,
        _parser: ArgumentParser,
        namespace: t.Any,
        values: str | t.Sequence[t.Any] | None,
        _option_string: str | None = None,
    ) -> None:
        if values is None:
            return
        value = self._enum(values)
        setattr(namespace, self.dest, value)


class TimeDirection(Enum):  # TODO: Future Task: StrEnum was 3.11 or so
    """Use this enum for describing the time direction.

    Supported output types are:

    ====== =============================
    Type   Description
    ====== =============================
    future Events must lie in the past
    past   Events must lie in the future
    ====== =============================

    """

    FUTURE = "future"
    PAST = "past"


class ArgparseActionDateParser(Action):
    """Custom argparse action for `datetime`."""

    def __init__(  # type: ignore[no-untyped-def]
        self,
        time_direction: None | TimeDirection = None,
        input_timezone: t.Callable[[], tzinfo] | None = None,
        output_timezone: t.Callable[[], tzinfo] | None = None,
        **kwargs,  # noqa: ANN003
    ) -> None:
        _time_direction: TimeDirection = time_direction or TimeDirection.PAST
        _input_timezone: t.Callable[[], tzinfo] = input_timezone or tzlocal
        _output_timezone: t.Callable[[], tzinfo] = output_timezone or (
            lambda: timezone.utc
        )

        self.input_timezone: tzinfo = _input_timezone()
        self.output_timezone: tzinfo = _output_timezone()

        settings: dateparser._Settings = {
            "PREFER_DATES_FROM": _time_direction.value,
            "TIMEZONE": str(self.input_timezone),
            "TO_TIMEZONE": str(self.output_timezone),
            "RETURN_AS_TIMEZONE_AWARE": True,
        }

        self._parser: partial[datetime | None] = partial(
            dateparser.parse,
            settings=settings,
        )
        self.time_direction: TimeDirection = _time_direction

        super().__init__(**kwargs)

    def __call__(  # noqa: D102
        self,
        _parser: ArgumentParser,
        namespace: t.Any,
        values: str | t.Sequence[t.Any] | None,
        _option_string: str | None = None,
    ) -> None:
        if values is None:
            return

        dt: datetime | None = self._parser(str(values))
        if dt is None:
            err_msg = (
                "The datetime parser was unable to determine the entered date."
            )
            raise TypeError(err_msg)

        dt_now = datetime.now(self.output_timezone)
        match self.time_direction:
            case TimeDirection.FUTURE:
                if dt <= dt_now:
                    err_msg = "The date must be in the future."
                    raise ValueError(err_msg)
            case TimeDirection.PAST:
                if dt > dt_now:
                    err_msg = "The date must be in the past."
                    raise ValueError(err_msg)

        setattr(namespace, self.dest, dt)
