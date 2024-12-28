# Changelog


All notable changes to MatrixCtl will be documented in this file.


You can find the issue tracker on
[GitHub](https://github.com/MichaelSasser/matrixctl/issues).

## 0.12.1-beta.1 - 2024-12-28

### 🏗️ Breaking changes

### ⚙️ Miscellaneous Tasks

#### Classifiers

- Add 3.12

#### Dependabot

- Remove Dependabot config as we use Renovate from now on

#### Deps

- Update pypa/gh-action-pypi-publish action to v1.8.14
- Update pandoc/core docker tag to v2.19.2
- Update dependency ubuntu to v22
- Update pandoc/core docker tag to v3
- Update softprops/action-gh-release action to v2
- Update actions/checkout action to v4.1.7
- Update dependency ruff to v0.4.9
- Update pypa/gh-action-pypi-publish action to v1.9.0
- Update dependency flake8 to v7.1.0
- Update dependency sphinx-autodoc-typehints to v2.2.0
- Update dependency ruff to v0.4.10
- Update dependency sphinx-autodoc-typehints to v2.2.1
- Update dependency sphinx-autodoc-typehints to v2.2.2
- Update dependency coverage to v7.5.4
- Update dependency mypy to v1.10.1
- Update dependency pylint to v3.2.4
- Update pandoc/core docker tag to v3.2.1
- Update dependency pylint to v3.2.5
- Update actions/setup-python action to v5.1.1
- Update dependency tox to v4.16.0
- Update dependency ruff to v0.5.1
- Update dependency coverage to v7.6.0
- Update pandoc/core docker tag to v3.3.0
- Update actions/setup-python action to v5.2.0
- Update snok/install-poetry action to v1.4
- Update pypa/gh-action-pypi-publish action to v1.10.1
- Update pandoc/core docker tag to v3.4.0
- Update pypa/gh-action-pypi-publish action to v1.10.2
- Update dependency ruff to v0.6.8
- Update dependency vulture to v2.12
- Update dependency ubuntu to v24
- Update actions/checkout action to v4.2.0
- Update dependency pylint to v3.3.1
- Update dependency tox to v4.20.0
- Update dependency types-setuptools to v75
- Update pypa/gh-action-pypi-publish action to v1.10.3
- Update dependency ruff to v0.6.9
- Update dependency tox to v4.21.2
- Update dependency vulture to v2.13
- Update actions/cache action to v4.1.0
- Update dependency pre-commit to v4
- Update actions/checkout action to v4.2.1
- Update pandoc/core docker tag to v3.5.0
- Update dependency pre-commit to v4.0.1
- Update actions/checkout action to v4.2.1 ([#856](https://github.com/MichaelSasser/matrixctl/issues/856))
- Update actions/checkout action to v4.2.2 ([#857](https://github.com/MichaelSasser/matrixctl/issues/857))
- Update astral-sh/setup-uv action to v5 ([#860](https://github.com/MichaelSasser/matrixctl/issues/860))
- Lock file maintenance ([#861](https://github.com/MichaelSasser/matrixctl/issues/861))

### 🚀 Features

#### Addon

- Add download command

#### Ci

- Add codeql workflow

### 🐛 Bug Fixes

#### Ci

- Replace master/develop branch with main branch
- Rye run sync regardless of cache hit; remove old codeql workflow
- Add `tomli` since it seems to be required for ci to build the docs
- Use a version matrix and let rye pin the python version
- Create `.python-version` before installing rye to avoid multiple toolchains
- Remove `--no-lock` from `rye sync`
- Wrap make for docs in 'uv run'

#### Deps

- Update dependency psycopg to v3.2.1
- Update dependency psycopg to v3.2.2
- Update dependency paramiko to v3.5.0
- Update dependency psycopg to v3.2.3
- Update dependency rich to v13.9.2

#### Docs

- Add docs for the download feature
- Replace master branch with main branch
- Wrap make in 'uv run'

#### Pre-commit

- Ignore all `lock` files

#### Renovate

- Add missing `:`

### 📚 Documentation

#### Changelog

- Make the old changelog available under changelog

#### Readme

- Typo

## 0.12.0 - 2024-06-05

### ⚙️ Miscellaneous Tasks

#### Dependencies

- Update mypy v0.991 -> v1.1.1
- Bump sphinx v5.2.3 -> v6.1.3
- Bump xdg v5.1.1 -> v6.0.0
- Bump paramiko v2.11.0 -> v3.1.0
- Bump some linters

#### Matrixctl

- Bump version from v0.12.0-beta.2 to v0.12.0

#### Pre-commit

- Update sources

### 🚀 Features

### 🐛 Bug Fixes

#### Ci

- Use Python 3.11 in CI

#### Deepsource

- Add skipcq: PYL-W0212 for intentionally use of private type _SubParsersAction

#### Largest-rooms

- Use processed variable to produce output for table instead of the input variable

#### Rtd

- Add '--all-extras' to the install arguments
- Follow the latest guidelines

## 0.12.0-beta.2 - 2023-03-23

### ⚙️ Miscellaneous Tasks

#### Workflow

- Update Python 3.9 -> 3.10
- Fix Python version

### 🚀 Features

#### Tests

- Add tests for sanitizers

### 🐛 Bug Fixes

#### Ssh

- Lazy formatting of message string passed to logging module

#### Table

- Use correct types in docs

#### Tox

- Update label from py39 -> py310

#### Yaml

- Don't log the database password for synapse in debug mode

## 0.12.0-beta.1 - 2021-12-02

### ⚙️ Miscellaneous Tasks

### 🐛 Bug Fixes

#### Api

- Remove f-string without any expression

#### Doctest

- Ignore example (not meant as doctest)

#### Purge-remote-media

- Message rooms -> media files

#### Table

- Error when table_data is empty
- Dicstring

## 0.11.4 - 2021-12-01

### ⚙️ Miscellaneous Tasks

#### Pre-commit

- Update dependencies

### 🐛 Bug Fixes

#### Api

- Typehints

## 0.11.3 - 2021-11-16

### 🚀 Features

#### README

- Update help output

#### Action

- Generate the release body with a script

#### Delroom

- Update delroom to use the "Delete Room API"

#### Help

- Debloat

#### Purge-history

- Add  switch

#### Rooms

- Add  switch argument

### 🐛 Bug Fixes

#### Users

- Set timeout to 10s

## 0.11.2 - 2021-09-26

### 🐛 Bug Fixes

## 0.10.1 - 2021-06-17

### 🐛 Bug Fixes

## 0.9.0 - 2021-04-23

### 📚 Documentation

## 0.8.6 - 2021-04-17

### 🚀 Features

### 🐛 Bug Fixes

### 📚 Documentation

<!-- generated by git-cliff -->
