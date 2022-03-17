OT_PYTHON ?= python
pipenv_envvars := $(and $(CI),PIPENV_IGNORE_VIRTUALENVS=1)
pipenv := $(pipenv_envvars) $(OT_PYTHON) -m pipenv
python := $(pipenv) run python
clean_cmd = $(SHX) rm -rf build dist .coverage coverage.xml '*.egg-info' '**/__pycache__' '**/*.pyc' '**/.mypy_cache'
SHX := npx shx
pipenv_opts := --dev


EMULATION_SYSTEM_DIR := emulation_system

SUB = {SUB}

EMULATION_SYSTEM_CMD := (cd ./emulation_system && pipenv run python main.py emulation-system {SUB} -)
REMOTE_ONLY_EMULATION_SYSTEM_CMD := (cd ./emulation_system && pipenv run python main.py emulation-system {SUB} - --remote-only)
COMPOSE_BUILD_COMMAND := docker buildx bake --file tmp-compose.yaml
COMPOSE_RUN_COMMAND := docker-compose -f - up
COMPOSE_KILL_COMMAND := docker-compose -f - kill
COMPOSE_REMOVE_COMMAND := docker-compose -f - rm --force
COMPOSE_LOGS_COMMAND := docker-compose -f - logs -f
COMPOSE_RESTART_COMMAND := docker-compose -f - restart --timeout 1

abs_path := $(realpath ${file_path})


.PHONY: build
build:
	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} > ~/tmp-compose.yaml
	./scripts/makefile/helper_scripts/build.sh ~/tmp-compose.yaml
	@rm ~/tmp-compose.yaml

.PHONY: run
run:
	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_RUN_COMMAND)

.PHONY: restart
restart:
	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_RESTART_COMMAND)


.PHONY: run-detached
run-detached:
	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_RUN_COMMAND) -d


.PHONY: remove
remove:
	$(if $(file_path),@echo "Removing system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_KILL_COMMAND)
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_REMOVE_COMMAND)

.PHONY: remove-build-run
remove-build-run:
	$(if $(file_path),@echo "Removing system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory remove file_path=${abs_path}
	@$(MAKE) --no-print-directory build file_path=${abs_path}
	@$(MAKE) --no-print-directory run file_path=${abs_path}

.PHONY: remove-build-run-detached
remove-build-run-detached:
	$(if $(file_path),@echo "Removing system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory remove file_path=${abs_path}
	@$(MAKE) --no-print-directory build file_path=${abs_path}
	@$(MAKE) --no-print-directory run-detached file_path=${abs_path}


.PHONY: logs
logs:
	$(if $(file_path),@echo "Printing logs from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path}  | $(COMPOSE_LOGS_COMMAND)

.PHONY: logs-follow
logs-follow:
	$(if $(file_path),@echo "Printing logs from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path}  | $(COMPOSE_LOGS_COMMAND) --tail 100

.PHONY: generate-compose-file
generate-compose-file:
	$(if $(file_path),,$(error file_path variable required))
	@$(subst $(SUB), ${abs_path}, $(EMULATION_SYSTEM_CMD))

.PHONY: check-remote-only
check-remote-only:
	$(if $(file_path),,$(error file_path variable required))
	@$(subst $(SUB), ${abs_path}, $(REMOTE_ONLY_EMULATION_SYSTEM_CMD)) > /dev/null
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


.PHONY: load-containers
load-containers:
	$(if $(file_path),,$(error file_path variable required))
	$(if $(filter),,$(error filter variable required))
	@(cd ./emulation_system && pipenv run python main.py load-containers "${abs_path}" "${filter}")

.PHONY: local-load-containers
local-load-containers:
	$(if $(file_path),,$(error file_path variable required))
	$(if $(filter),,$(error filter variable required))
	@(cd ./emulation_system && pipenv run python main.py load-containers --local-only "${abs_path}" "${filter}")


.PHONY: can-comm
can-comm:
	$(if $(file_path),,$(error file_path variable required))
	@$(MAKE) \
		--no-print-directory \
		load-containers \
		file_path="${abs_path}" \
		filter="can-server" \
		| xargs -o -I{} docker exec -it {} python3 -m opentrons_hardware.scripts.can_comm --interface opentrons_sock


.PHONY: can-mon
can-mon:
	$(if $(file_path),,$(error file_path variable required))
	@$(MAKE) \
		--no-print-directory \
		load-containers \
		file_path="${abs_path}" \
		filter="can-server" \
		| xargs -o -I{} docker exec -it {} python3 -m opentrons_hardware.scripts.can_mon --interface opentrons_sock
