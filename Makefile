#
# Makefile: Commands to simplify development and releases
#
# Usage:
#
#    make clean
#    make checks
#    make test-all
#    make patch

# You can set these variable on the command line.
PYTHON = python3.8

# Where everything lives
site_python := /usr/bin/env $(PYTHON)

root_dir := $(realpath .)
venv_dir = $(root_dir)/.venv
app_dir = $(root_dir)/lynx

python = $(venv_dir)/bin/python3
pip = $(venv_dir)/bin/pip3
pip-compile = $(venv_dir)/bin/pip-compile
pip-sync = $(venv_dir)/bin/pip-sync
django = $(python) $(root_dir)/manage.py
checker = $(venv_dir)/bin/flake8
black = $(venv_dir)/bin/black
isort = $(venv_dir)/bin/isort
pytest = $(venv_dir)/bin/pytest
coverage = $(venv_dir)/bin/coverage
bumpversion = $(venv_dir)/bin/bump2version
tox = $(venv_dir)/bin/tox

commit_opts := --gpg-sign
upload_opts := --skip-existing --sign
pytest_opts := --flake8 --black --isort

# include any local makefiles
-include *.mk

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "  help                 to show this list"
	@echo "  clean-docs           to clean the generated HTML documentation"
	@echo "  clean-tests          to clean the directories created during testing"
	@echo "  clean-coverage       to clean the test coverage data and reports"
	@echo "  clean-venv           to clean the virtualenv"
	@echo "  clean                to clean everything EXCEPT the virtualenv"
	@echo
	@echo "  checks               to run quality code checks"
	@echo "  coverage             to measure the test coverage"
	@echo "  docs                 to build the HTML documentation"
	@echo "  install              to install the dependencies in the virtualenv"
	@echo "  major                to update the version number for a major release, e.g. 2.1 to 3.0"
	@echo "  messages             to run the makemessages and compilemessages management commands"
	@echo "  migrate              to run migrate management command"
	@echo "  migrations           to run makemigrations management command"
	@echo "  minor                to update the version number for a minor release, e.g. 2.1 to 2.2"
	@echo "  patch                to update the version number for a patch release, e.g. 2.1.1 to 2.1.2"
	@echo "  runserver            to run the Django demo site"
	@echo "  test                 to run the tests during development"
	@echo "  test-all             to run the tests for all the supported environments"
	@echo "  venv                 to create the virtualenv"
	@echo

.PHONY: clean-docs
clean-docs:
	cd docs && make clean

.PHONY: clean-tests
clean-tests:
	rm -rf .tox
	rm -rf .pytest_cache

.PHONY: clean-coverage
clean-coverage:
	rm -rf .coverage
	rm -rf reports/coverage

.PHONY: clean-venv
clean-venv:
	rm -rf $(venv_dir)

.PHONY: clean
clean: clean-tests clean-coverage clean-docs

.PHOMY: checks
checks:
	$(checker) $(app_dir)
	$(black) --check $(app_dir)
	$(isort) --check $(app_dir)

.PHONY: coverage
coverage:
	$(pytest) --cov=lynx --cov-config=setup.cfg --cov-report html

.PHONY: docs
docs:
	cd docs && make html

.PHONY: install
install:
	$(pip) install --upgrade pip setuptools wheel
	$(pip) install pip-tools
	$(pip-sync) requirements/dev.txt

.PHONY: major
major:
	$(bumpversion) major

.PHONY: messages
messages:
	cd $(app_dir) && $(django) makemessages --no-obsolete --all && $(django) compilemessages

.PHONY: migrate
migrate:
	$(django) migrate

.PHONY: migrations
migrations:
	$(django) makemigrations

.PHONY: minor
minor:
	$(bumpversion) minor

.PHONY: patch
patch:
	$(bumpversion) patch

.PHONY: runserver
runserver: venv
	$(django) migrate
	$(django) runserver

.PHONY: test
test:
	$(pytest) $(pytest_opts)

.PHONY: test-all
test-all: test
	$(tox)
	$(tox) -e docs

.PHONY: venv
venv:
	$(site_python) -m venv $(venv_dir)
