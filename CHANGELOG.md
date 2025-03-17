# Changelog


All notable changes to MatrixCtl will be documented in this file.


You can find the issue tracker on
[GitHub](https://github.com/MichaelSasser/matrixctl/issues).

## [0.14.1](https://github.com/MichaelSasser/matrixctl/compare/v0.14.0...v0.14.1) (2025-03-17)


### Features

* **rows:** render avatars in membership events ([d152b44](https://github.com/MichaelSasser/matrixctl/commit/d152b441d8aa1001549aadd9c83133e0045941c0))


### Bug Fixes

* **deps:** update dependency sphinx-autodoc-typehints to &gt;=3,&lt;3.2 ([#875](https://github.com/MichaelSasser/matrixctl/issues/875)) ([53371db](https://github.com/MichaelSasser/matrixctl/commit/53371db52faa94df0123ab25ad5f352959d91927))


### Miscellaneous Chores

* release 0.14.1 ([bf27865](https://github.com/MichaelSasser/matrixctl/commit/bf27865c3dceb771eff9d0c5ba4c8cf27c14d88c))

## [0.14.0](https://github.com/MichaelSasser/matrixctl/compare/v0.13.0...v0.14.0) (2025-01-12)


### Features

* put the functionallity for rendering an image in terminal from a mxc into its own helper function ([2053965](https://github.com/MichaelSasser/matrixctl/commit/2053965b9ffa6ff4b1b68b4d20bb64c692841c75))


### Bug Fixes

* **ci:** add manifest, move 'extra-files' into config ([7a96f38](https://github.com/MichaelSasser/matrixctl/commit/7a96f38a57521ad108d5e30bd780bb210651a939))
* **deps:** update dependency sphinx-autodoc-typehints to v3 ([#866](https://github.com/MichaelSasser/matrixctl/issues/866)) ([4192c74](https://github.com/MichaelSasser/matrixctl/commit/4192c74970b1da55d29d2e9185230d7e586a52a7))
* **get-events:** use  instead of ([04d90bf](https://github.com/MichaelSasser/matrixctl/commit/04d90bfc2c34f4f27491b3a2855059aec17bd108))
* **pre-commit:** disable pycln ([03eb8ba](https://github.com/MichaelSasser/matrixctl/commit/03eb8ba0688e571f3371ce635bb2068b209da4b6))
* **release:** also update version in lock file ([d03a5f1](https://github.com/MichaelSasser/matrixctl/commit/d03a5f1c3abd0519de6af91a02ccb42843218517))

## [0.13.0](https://github.com/MichaelSasser/matrixctl/compare/v0.13.0...v0.13.0) (2024-12-31)


### Features

* **get-events:** Add option to format events as rows, with image support ([#859](https://github.com/MichaelSasser/matrixctl/issues/859)) ([339fcad](https://github.com/MichaelSasser/matrixctl/commit/339fcad8ada0e2117e807487730e566554aa3f0c))
* **rows:** make images in rows configurable ([253b632](https://github.com/MichaelSasser/matrixctl/commit/253b632e618b8e275ce8b972e62a01f1dc5ab9fd))
* try out release-please ([80363a9](https://github.com/MichaelSasser/matrixctl/commit/80363a9c3965cf53cc2ef27f284a9bac45f624fc))


### Documentation

* **readme:** Improve wording ([007e292](https://github.com/MichaelSasser/matrixctl/commit/007e292d745d5325ad3a079c8c2d4a32f929653f))


### Miscellaneous Chores

* release 0.13.0 ([5ac62f4](https://github.com/MichaelSasser/matrixctl/commit/5ac62f4fa4edd788144ed7b2be1f3f592ea92d64))
* release 0.13.0b3 ([b152e4b](https://github.com/MichaelSasser/matrixctl/commit/b152e4bcb360ebf5ef95e0ccc4ee452eb91c9cca))

## [0.12.1b2] - 2024-12-28

### 🐛 Bug Fixes

- Move versioning from semver to PyPA spec due to normalization

## [0.12.1-beta.1] - 2024-12-28

### 🏗️ Breaking changes

- Remove Jitsi related features.

### ⚙️ Miscellaneous Tasks

- *(deps)* Update pypa/gh-action-pypi-publish action to v1.8.14
- *(deps)* Update pandoc/core docker tag to v2.19.2
- *(deps)* Update dependency ubuntu to v22
- *(deps)* Update pandoc/core docker tag to v3
- *(deps)* Update softprops/action-gh-release action to v2
- *(dependabot)* Remove Dependabot config as we use Renovate from now on
- *(classifiers)* Add 3.12
- *(deps)* Update actions/checkout action to v4.1.7
- *(deps)* Update dependency ruff to v0.4.9
- *(deps)* Update pypa/gh-action-pypi-publish action to v1.9.0
- *(deps)* Update dependency flake8 to v7.1.0
- *(deps)* Update dependency sphinx-autodoc-typehints to v2.2.0
- *(deps)* Update dependency ruff to v0.4.10
- *(deps)* Update dependency sphinx-autodoc-typehints to v2.2.1
- *(deps)* Update dependency sphinx-autodoc-typehints to v2.2.2
- *(deps)* Update dependency coverage to v7.5.4
- *(deps)* Update dependency mypy to v1.10.1
- *(deps)* Update dependency pylint to v3.2.4
- *(deps)* Update pandoc/core docker tag to v3.2.1
- *(deps)* Update dependency pylint to v3.2.5
- *(deps)* Update actions/setup-python action to v5.1.1
- *(deps)* Update dependency tox to v4.16.0
- *(deps)* Update dependency ruff to v0.5.1
- *(deps)* Update dependency coverage to v7.6.0
- *(deps)* Update pandoc/core docker tag to v3.3.0
- *(deps)* Update actions/setup-python action to v5.2.0
- *(deps)* Update snok/install-poetry action to v1.4
- *(deps)* Update pypa/gh-action-pypi-publish action to v1.10.1
- *(deps)* Update pandoc/core docker tag to v3.4.0
- *(deps)* Update pypa/gh-action-pypi-publish action to v1.10.2
- *(deps)* Update dependency ruff to v0.6.8
- *(deps)* Update dependency vulture to v2.12
- *(deps)* Update dependency ubuntu to v24
- *(deps)* Update actions/checkout action to v4.2.0
- *(deps)* Update dependency pylint to v3.3.1
- *(deps)* Update dependency tox to v4.20.0
- *(deps)* Update dependency types-setuptools to v75
- *(deps)* Update pypa/gh-action-pypi-publish action to v1.10.3
- *(deps)* Update dependency ruff to v0.6.9
- *(deps)* Update dependency tox to v4.21.2
- *(deps)* Update dependency vulture to v2.13
- *(deps)* Update actions/cache action to v4.1.0
- *(deps)* Update dependency pre-commit to v4
- *(deps)* Update actions/checkout action to v4.2.1
- *(deps)* Update pandoc/core docker tag to v3.5.0
- *(deps)* Update dependency pre-commit to v4.0.1
- *(deps)* Update actions/checkout action to v4.2.1 ([#856](https://github.com/MichaelSasser/matrixctl/issues/856))
- Update dependencies
- *(deps)* Update actions/checkout action to v4.2.2 ([#857](https://github.com/MichaelSasser/matrixctl/issues/857))
- *(deps)* Update astral-sh/setup-uv action to v5 ([#860](https://github.com/MichaelSasser/matrixctl/issues/860))
- *(deps)* Lock file maintenance ([#861](https://github.com/MichaelSasser/matrixctl/issues/861))
- Bump version from v0.12.0 to v0.12.1-beta.1

### 🚀 Features

- *(addon)* Add download command
- Remove unused dependencies
- Add `rye run doc` command for building the docs
- [**breaking**] Move from git-flow to GitHub Flow branching model
- Rename addons to commands and remove `api_path` as well as `api_version` from the API handler
- *(ci)* Add codeql workflow

### 🐛 Bug Fixes

- *(deps)* Update dependency psycopg to v3.2.1
- *(docs)* Add docs for the download feature
- Break out the the sync status code handler from `_request` of the API handler into `handle_sync_response_status_code` and re-use it in `streamed_download`
- *(renovate)* Add missing `:`
- *(deps)* Update dependency psycopg to v3.2.2
- *(deps)* Update dependency paramiko to v3.5.0
- *(deps)* Update dependency psycopg to v3.2.3
- *(deps)* Update dependency rich to v13.9.2
- *(docs)* Replace master branch with main branch
- *(ci)* Replace master/develop branch with main branch
- *(ci)* Rye run sync regardless of cache hit; remove old codeql workflow
- *(ci)* Add `tomli` since it seems to be required for ci to build the docs
- Add dependency `exceptiongroup` for python < 3.11 to build docs
- *(ci)* Use a version matrix and let rye pin the python version
- *(ci)* Create `.python-version` before installing rye to avoid multiple toolchains
- *(ci)* Create `.python-version` before installing rye to avoid multiple toolchains
- *(ci)* Remove `--no-lock` from `rye sync`
- *(ci)* Remove `--no-lock` from `rye sync`
- *(docs)* Wrap make in 'uv run'
- *(ci)* Wrap make for docs in 'uv run'
- *(pre-commit)* Ignore all `lock` files

### 📚 Documentation

- *(changelog)* Make the old changelog available under changelog
- Replace rye with uv
- *(readme)* Typo

## [0.12.0] - 2024-06-05

### ⚙️ Miscellaneous Tasks

- *(dependencies)* Update mypy v0.991 -> v1.1.1
- *(dependencies)* Bump sphinx v5.2.3 -> v6.1.3
- *(dependencies)* Bump xdg v5.1.1 -> v6.0.0
- *(dependencies)* Bump paramiko v2.11.0 -> v3.1.0
- *(dependencies)* Bump some linters
- Update all dependencies
- Update ruff, towncrier pylint yapf attrs, httpx, ruamel.ymal
- *(pre-commit)* Update sources
- *(matrixctl)* Bump version from v0.12.0-beta.2 to v0.12.0

### 🚀 Features

- Use ruff instead of flake8 and isort (and addons); refactor
- Update pre-commit, also run tests on 3.11
- Add largest-rooms command

### 🐛 Bug Fixes

- *(deepsource)* Add skipcq: PYL-W0212 for intentionally use of private type _SubParsersAction
- *(largest-rooms)* Use processed variable to produce output for table instead of the input variable
- Build process due to poetry having new optional group config
- *(ci)* Use Python 3.11 in CI
- Make linters happy
- *(rtd)* Add '--all-extras' to the install arguments
- *(rtd)* Follow the latest guidelines

## [0.12.0-beta.2] - 2023-03-23

### ⚙️ Miscellaneous Tasks

- Update dependencies
- *(workflow)* Update Python 3.9 -> 3.10
- *(workflow)* Fix Python version
- Update pre-commit dependencies
- Update poetry lock file
- Bump version from v0.12.0-beta.1 to v0.12.0-beta.2
- Bump version from v0.12.0-beta.1 to v0.12.0-beta.2

### 🚀 Features

- *(tests)* Add tests for sanitizers
- Add force-purge argument to delroom

### 🐛 Bug Fixes

- Lazy formatting of message string passed to logging module
- False positive BAN-B601
- *(ssh)* Lazy formatting of message string passed to logging module
- *(tox)* Update label from py39 -> py310
- *(yaml)* Don't log the database password for synapse in debug mode
- Formatting strings passed to logging module
- Formatting strings passed to logging module
- *(table)* Use correct types in docs
- Formatted string passed to logging module

## [0.12.0-beta.1] - 2021-12-02

### ⚙️ Miscellaneous Tasks

- Add breaking newsfragment

### 🐛 Bug Fixes

- *(purge-remote-media)* Message rooms -> media files
- *(purge-remote-media)* Message rooms -> media files
- *(doctest)* Ignore example (not meant as doctest)
- *(api)* Remove f-string without any expression
- *(table)* Error when table_data is empty
- *(table)* Dicstring

## [0.11.4] - 2021-12-01

### ⚙️ Miscellaneous Tasks

- *(pre-commit)* Update dependencies

### 🐛 Bug Fixes

- *(api)* Typehints

## [0.11.3] - 2021-11-16

### 🚀 Features

- Implement make-room-admin API
- Implement get context API
- *(rooms)* Add  switch argument
- *(purge-history)* Add  switch
- Implement
- Implement delete-local-media addon
- *(delroom)* Update delroom to use the "Delete Room API"
- *(help)* Debloat
- *(README)* Update help output
- *(action)* Generate the release body with a script
- Add missing newsfragment and reorder release workflow

### 🐛 Bug Fixes

- *(users)* Set timeout to 10s
- Wrap long line

## [0.11.2] - 2021-09-26

### 🐛 Bug Fixes

- Unguarded next()

## [0.10.1] - 2021-06-17

### 🐛 Bug Fixes

- Use secure, temporary directory for ansible_runner's private data ([#120](https://github.com/MichaelSasser/matrixctl/issues/120))

## [0.9.0] - 2021-04-23

### 📚 Documentation

- Add xref param type links
- Fix commandline example ([#77](https://github.com/MichaelSasser/matrixctl/issues/77))
- Remove program name from changelog ([#80](https://github.com/MichaelSasser/matrixctl/issues/80))

## [0.8.6] - 2021-04-17

### 🚀 Features

- __main__.py instead of application.py ([#62](https://github.com/MichaelSasser/matrixctl/issues/62))
- Add towncrier to generate a changelog ([#63](https://github.com/MichaelSasser/matrixctl/issues/63))

### 🐛 Bug Fixes

- Logging TypeError ([#45](https://github.com/MichaelSasser/matrixctl/issues/45)) ([#66](https://github.com/MichaelSasser/matrixctl/issues/66))

### 📚 Documentation

- Add changelog to docs
- Minor
- Add rest of docstrings; set min. coverage 100%

<!-- generated by git-cliff -->
