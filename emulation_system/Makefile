# opentrons emulation_system makefile
OT_PYTHON ?= python
pipenv_envvars := $(and $(CI),PIPENV_IGNORE_VIRTUALENVS=1)
pipenv := $(pipenv_envvars) $(OT_PYTHON) -m pipenv
python := $(pipenv) run python
pip := $(pipenv) run pip
pytest := $(pipenv) run py.test
pipenv_opts := --dev
SHX := npx shx


tests ?= tests
test_opts ?=  --cov=emulation_system --cov-report term-missing:skip-covered --cov-report xml:coverage.xml

# test modules to typecheck
tests_to_typecheck := \
	tests/

# Defined separately than the clean target so the wheel file doesn’t have to
# depend on a PHONY target
clean_cmd = $(SHX) rm -rf build dist .coverage coverage.xml '*.egg-info' '**/__pycache__' '**/*.pyc' '**/.mypy_cache'

.PHONY: setup
setup:
	$(pipenv) sync $(pipenv_opts)
	$(pipenv) run pip freeze

.PHONY: clean
clean:
	$(clean_cmd)

.PHONY: teardown
teardown:
	$(pipenv) --rm

.PHONY: test
test:
	$(pytest) $(tests) $(test_opts)

.PHONY: lint
lint:
	$(python) -m mypy emulation_system $(tests_to_typecheck)
	$(python) -m black --check emulation_system tests setup.py
	$(python) -m flake8 \
		--per-file-ignores="emulation_system/compose_file_creator/input/hardware_models/__init__.py:E501"  \
		emulation_system tests setup.py

.PHONY: format
format:
	$(python) -m black emulation_system tests setup.py