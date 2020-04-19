from __future__ import annotations

import re

from matrixctl import __version__


def test_version() -> None:
    """Test, if the version matches SemVer.

    The regular expression is form:
    https://semver.org/#is-there-a-suggested-regular-expression-regex-to-
            check-a-semver-string
    """
    # Setup
    desired = re.compile(
        r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\."
        r"(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-]"
        r"[0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
        r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    )

    # Exercise
    actual = __version__

    # Verify
    assert desired.fullmatch(actual)

    # Cleanup - None
