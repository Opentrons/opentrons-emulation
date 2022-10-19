.PHONY: update
update:
	poetry env use 3.10
	poetry update
	poetry install

.PHONY: setup
setup:
	poetry env use 3.10
	poetry install

.PHONY: clean
clean:
	rm -rf build dist .coverage coverage.xml '*.egg-info' '**/__pycache__' '**/*.pyc' '**/.mypy_cache'

.PHONY: teardown
teardown:
	poetry env info -p | xargs basename | xargs poetry env remove

.PHONY: test
test:
	poetry run py.test tests --cov=emulation_system --cov-report term-missing:skip-covered --cov-report xml:coverage.xml

.PHONY: lint
lint:
	poetry run python -m mypy emulation_system tests
	poetry run python -m isort --check --skip compose_file_model.py emulation_system tests
	poetry run python -m black --check --line-length 88 --force-exclude compose_file_model.py emulation_system tests
	poetry run python -m flake8 emulation_system tests
	poetry run python -m mdformat --check ../README.md ../docs

.PHONY: format
format:
	poetry run python -m black --line-length 88 --force-exclude compose_file_model.py emulation_system tests
	poetry run python -m isort --skip compose_file_model.py emulation_system tests
	poetry run python -m mdformat ../README.md ../docs
