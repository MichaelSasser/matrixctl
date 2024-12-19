.PHONY: all

all: help


##@
##@ Build Commands
##@

update: ##@ Update the dependencies to the ones defined
				##@ in the pyproject.toml [alias: u]
	uv sync --all-extras --upgrade

u: update

build: ##@ Build the application [alias: b]
	uv build

b: build

run: ##@ Build and run the application [alias: r]
	uv run matrixctl

r: run

##@
##@ Check Commands
##@


check: fmt lint test  ##@ Format, lint, run tests
											##@ [alias: c]

c: check

test: ##@ Run tests [alias: t]
	uv run coverage run -m pytest --doctest-modules

t: test

fmt: ##@ Format the project
	ruff format

lint: lint-toml lint-python lint-type ##@ Lint the the source code (Rust, TOML)

lint-toml: ##@  Lint all TOML files
	taplo lint --colors always

lint-python: ##@ Run ruff
	uv run ruff check

lint-type: ##@ Run basedpyright
	uv run basedpyright

tox: ##@ Run tox
	uv tool run tox

##@
##@ Documentation Related Commands
##@

doc: ##@ Build the documentation [alias: d]
	cargo doc --color always --bins --no-deps --frozen --examples --open --verbose --release

d: docs

changelog-unreleased: ##@ Preview the unreleased changes
	git cliff --unreleased

##@
##@ Misc commands
##@

lines:  ##@ Show lines of code
	tokei

help: ##@ This help message
	@printf "\nUsage: make <command>\n"
	@grep -F -h "##@" $(MAKEFILE_LIST) | grep -F -v grep -F | sed -e 's/\\$$//' | awk 'BEGIN {FS = ":*[[:space:]]*##@[[:space:]]*"}; \
	{ \
		if($$2 == "") \
			pass; \
		else if($$0 ~ /^#/) \
			printf "\n\n\033[1m%s\033[0m\n", $$2; \
		else if($$1 == "") \
			printf "     %-25s%s\n", "", $$2; \
		else \
			printf "\n    \033[34m%-25s\033[0m %s\n", $$1, $$2; \
	}'
