"""Nox is a command-line tool that automates testing.

It works in multiple Python environments, similar to tox. Unlike tox, Nox
uses a standard Python file for configuration.

It gets automatically installed by poetry.

To run all tests use the command ``nox``. Make sure you enabled the virtual
environment with ``poetry shell`` or run ``poetry run nox``

"""

from pathlib import Path
from textwrap import dedent

import nox


nox.options.reuse_existing_virtualenvs = True

PACKAGE = "matrixctl"
PYTHON_VERSIONS = ["3.10", "3.9"]


# https://github.com/cjolowicz/nox-poetry/blob/main/noxfile.py
def activate_virtualenv_in_precommit_hooks(session: nox.Session) -> None:
    """Activate virtualenv in hooks installed by pre-commit.

    This function patches git hooks installed by pre-commit to activate the
    session's virtual environment. This allows pre-commit to locate hooks in
    that environment when invoked from git.

    """
    assert session.bin is not None  # noqa: S101

    virtualenv = session.env.get("VIRTUAL_ENV")
    if virtualenv is None:
        return

    hookdir = Path(".git") / "hooks"
    if not hookdir.is_dir():
        return

    for hook in hookdir.iterdir():
        if hook.name.endswith(".sample") or not hook.is_file():
            continue

        text = hook.read_text()
        bindir = repr(session.bin)[1:-1]  # strip quotes
        if not (
            Path("A") == Path("a")
            and bindir.lower() in text.lower()
            or bindir in text
        ):
            continue

        lines = text.splitlines()
        if not (lines[0].startswith("#!") and "python" in lines[0].lower()):
            continue

        header = dedent(
            f"""\
            import os
            os.environ["VIRTUAL_ENV"] = {virtualenv!r}
            os.environ["PATH"] = os.pathsep.join((
                {session.bin!r},
                os.environ.get("PATH", ""),
            ))
            """
        )

        lines.insert(1, header)
        hook.write_text("\n".join(lines))


@nox.session(name="pre-commit", python=PYTHON_VERSIONS[0])
def pre_commit(session: nox.Session) -> None:
    """Run pre-commit."""
    # , "--show-diff-on-failure"
    args: list[str] = session.posargs or [
        "run",
        "--all-files",
    ]
    session.install("pre-commit")
    session.run("pre-commit", *args)
    if args and args[0] == "install":
        activate_virtualenv_in_precommit_hooks(session)


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Run Pytest."""
    session.install(".")
    session.install(
        "pytest",
        "coverage[toml]",
        "pytest",
        "pytest-datadir",
        "pygments",
        "typing_extensions",
    )
    try:
        session.run(
            "coverage", "run", "--parallel", "-m", "pytest", *session.posargs
        )
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])


@nox.session
def coverage(session: nox.Session) -> None:
    """Produce the coverage report."""
    args: list[str] = session.posargs or ["report"]

    session.install("coverage[toml]")

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@nox.session(python=PYTHON_VERSIONS[0])
def interrogate(session: nox.Session) -> None:
    """Run interrogate."""
    session.install(".")
    session.install(
        "interrogate",
    )
    session.run("interrogate", PACKAGE, *session.posargs)


@nox.session(python=PYTHON_VERSIONS)
def docs(session: nox.Session) -> None:
    """Build the documentation."""
    session.install(".")
    session.install(
        "sphinx",
        "sphinx_autodoc_typehints",
        "sphinxcontrib-programoutput",
        "numpydoc",
        "sphinx_rtd_theme",
        "pytest",
    )
    session.run(
        "sphinx-build",
        "-T",
        "-W",
        "-b",
        "html",
        # "-d",
        "docs/source",
        "docs/build/html",
    )


@nox.session(python="3.10")
def safety(session: nox.Session) -> None:
    """Scan dependencies for insecure packages."""
    args: list[str] = session.posargs or ["check", "--full-report"]
    session.install("safety")
    session.run("safety", *args)


@nox.session(python=PYTHON_VERSIONS[0])
def changelogs(session: nox.Session) -> None:
    """Show a draft for the upcoming changelog."""
    args: list[str] = session.posargs or ["--draft"]
    session.install("towncrier")
    session.run("towncrier", *args)


# @nox.session(python=PYTHON_VERSIONS[0])
# def typeguard(session: nox.Session) -> None:
#     """Runtime type checking using Typeguard."""
#     session.install(".")
#     session.install("pytest", "typeguard", "pygments")
#     session.run(
#         "pytest",
#         f"--typeguard-packages={PACKAGE}",
#         "--verbose",
#         *session.posargs,
#     )


# @nox.session(python=PYTHON_VERSIONS[0])
# def xdoctest(session: nox.Session) -> None:
#     """Run examples with xdoctest."""
#     args = session.posargs or ["all"]
#     session.install(".")
#     session.install("xdoctest[colors]")
#     session.run("python", "-m", "xdoctest", PACKAGE, *args)
