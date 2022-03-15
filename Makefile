OT_PYTHON ?= python
pipenv_envvars := $(and $(CI),PIPENV_IGNORE_VIRTUALENVS=1)
pipenv := $(pipenv_envvars) $(OT_PYTHON) -m pipenv
python := $(pipenv) run python
clean_cmd = $(SHX) rm -rf build dist .coverage coverage.xml '*.egg-info' '**/__pycache__' '**/*.pyc' '**/.mypy_cache'
SHX := npx shx
pipenv_opts := --dev


include ./scripts/makefile/rebuilding.mk

EMULATION_SYSTEM_DIR := emulation_system

SUB = {SUB}

EMULATION_SYSTEM_CMD := (cd ./emulation_system && pipenv run python main.py emulation-system {SUB} -)
REMOTE_ONLY_EMULATION_SYSTEM_CMD := (cd ./emulation_system && pipenv run python main.py emulation-system {SUB} - --remote-only)
COMPOSE_BUILD_COMMAND := docker buildx bake --file tmp-compose.yaml
COMPOSE_RUN_COMMAND := docker-compose -f - up
COMPOSE_KILL_COMMAND := docker-compose -f - kill
COMPOSE_REMOVE_COMMAND := docker-compose -f - rm --force
COMPOSE_LOGS_COMMAND := docker-compose -f - logs -f


.PHONY: build-amd64
build-amd64:
	# TODO: Remove tmp file creation when Buildx 0.8.0 is released.
	# PR: https://github.com/docker/buildx/milestone/11
	# Ticket: https://github.com/docker/buildx/pull/864
	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${file_path}  > tmp-compose.yaml && $(COMPOSE_BUILD_COMMAND)
	@rm tmp-compose.yaml

.PHONY: build-arm64
build-arm64:
	# TODO: Remove tmp file creation when Buildx 0.8.0 is released.
	# PR: https://github.com/docker/buildx/milestone/11
	# Ticket: https://github.com/docker/buildx/pull/864
	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${file_path} > tmp-compose.yaml && $(COMPOSE_BUILD_COMMAND) --set *.platform=linux/x86_64
	@rm tmp-compose.yaml

.PHONY: run
run:
	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${file_path} | $(COMPOSE_RUN_COMMAND)


.PHONY: run-detached
run-detached:
	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${file_path} | $(COMPOSE_RUN_COMMAND) -d


.PHONY: remove
remove:
	$(if $(file_path),@echo "Removing system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${file_path} | $(COMPOSE_KILL_COMMAND)
	@$(MAKE) --no-print-directory generate-compose-file file_path=${file_path}  | $(COMPOSE_REMOVE_COMMAND)


.PHONY: logs
logs:
	$(if $(file_path),@echo "Printing logs from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${file_path}  | $(COMPOSE_LOGS_COMMAND)

.PHONY: generate-compose-file
generate-compose-file:
	$(if $(file_path),,$(error file_path variable required))
	@$(subst $(SUB), $(file_path), $(EMULATION_SYSTEM_CMD))

.PHONY: check-remote-only
check-remote-only:
	$(if $(file_path),,$(error file_path variable required))
	@$(subst $(SUB), $(file_path), $(REMOTE_ONLY_EMULATION_SYSTEM_CMD)) > /dev/null
	@echo "All services are remote"

.PHONY: setup
setup:
	$(pipenv) sync $(pipenv_opts)
	$(pipenv) run pip freeze
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) setup


.PHONY: clean
clean:
	$(clean_cmd)
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) clean


.PHONY: teardown
teardown:
	$(pipenv) --rm
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) teardown


.PHONY: lint
lint:
	$(python) -m mdformat --check .
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) lint


.PHONY: format
format:
	$(python) -m mdformat .
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) format


.PHONY: test
test:
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) test


.PHONY: test-samples
test-samples:
	@./scripts/makefile/helper_scripts/test_samples.sh


.PHONY: local-load-containers
local-load-containers:
	$(if $(file_path),,$(error file_path variable required))
	$(if $(filter),,$(error filter variable required))
	@(cd ./emulation_system && pipenv run python main.py load-local-containers "${file_path}" "${filter}")


.PHONY: can-comm
can-comm:
	$(if $(file_path),,$(error file_path variable required))
	@$(MAKE) \
		--no-print-directory \
		local-load-containers \
		file_path="${file_path}" \
		filter="can-server" \
		| xargs -o -I{} docker exec -it --workdir /opentrons/hardware {} python3 -m opentrons_hardware.scripts.can_comm --interface opentrons_sock


.PHONY: can-mon
can-mon:
	$(if $(file_path),,$(error file_path variable required))
	@$(MAKE) \
		--no-print-directory \
		local-load-containers \
		file_path="${file_path}" \
		filter="can-server" \
		| xargs -o -I{} docker exec -it --workdir /opentrons/hardware {} python3 -m opentrons_hardware.scripts.can_mon --interface opentrons_sock
