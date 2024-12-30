"""Custom argparse action classes."""

from __future__ import annotations

import typing as t

from argparse import Action
from argparse import ArgumentParser
from enum import Enum


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
