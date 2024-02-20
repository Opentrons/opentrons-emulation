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
	poetry env remove --all

.PHONY: test
test:
	poetry run pytest -vv tests/compose_file_creator --cov=emulation_system --cov-report term-missing:skip-covered --cov-report xml:coverage.xml

.PHONY: get-e2e-test-ids
get-e2e-test-ids:
	@poetry run python tests/e2e/scripts/e2e_interface.py get-test-ids

.PHONY: get-e2e-test-path
get-e2e-test-path:
	$(if $(test_id),,$(error test_id variable required))
	@poetry run python tests/e2e/scripts/e2e_interface.py get-test-path ${test_id}


.PHONY: execute-e2e-test
execute-e2e-test:
	$(if $(test_id),,$(error test_id variable required))
	poetry run pytest tests/e2e -k "${test_id}"


.PHONY: lint
lint:
	poetry run python -m mypy emulation_system tests
	poetry run ruff check .
	poetry run python -m black --check --line-length 88 --force-exclude compose_file_model.py emulation_system tests
	poetry run python -m mdformat --check ../README.md ../docs

.PHONY: format
format:
	poetry run python -m black --line-length 88 --force-exclude compose_file_model.py emulation_system tests
	poetry run ruff check --fix .
	poetry run python -m mdformat ../README.md ../docs
