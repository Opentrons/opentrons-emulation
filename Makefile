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

###########################################
####### Emulation Control Commands ########
###########################################

# Generates Docker-Compose file from passed configuration file and outputs it to stdout
.PHONY: generate-compose-file
generate-compose-file:

	$(if $(file_path),,$(error file_path variable required))
	@$(subst $(SUB), ${abs_path}, $(EMULATION_SYSTEM_CMD))


# Builds generated Docker-Compose file's necessary images using docker buildx
# Note 1: This repository supports building against `x86_64` and `arm64` type processors
#
# Note 2: Docker images should be rebuilt under the following conditions:
#
#	If anything changes in your configuration file
#	If you have an emulator using `remote` source type, `latest` source location, and there has been an update to the main branch of the source repo
#	If the underlying Dockerfile changes
.PHONY: build
build:

	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory --quiet generate-compose-file file_path=${abs_path} > ~/tmp-compose.yaml
	./scripts/makefile/helper_scripts/build.sh ~/tmp-compose.yaml
	@rm ~/tmp-compose.yaml

# Creates and starts Docker Containers from generated Docker-Compose file
# Outputs logs to stdout
# Stops and removes containers on exit of logs
.PHONY: run
run:

	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_RUN_COMMAND)

# Creates and starts Docker Containers from generated Docker-Compose file
# Detaches logs from stdout and returns control of terminal
.PHONY: run-detached
run-detached:

	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_RUN_COMMAND) -d

# Removes containers from generated Docker-Compose file
.PHONY: remove
remove:

	$(if $(file_path),@echo "Removing system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_KILL_COMMAND)
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_REMOVE_COMMAND)

# Removes, rebuilds, and runs generated Docker-Compose file
# Outputs logs to stdout
# Stops and removes containers on exit of logs
.PHONY: remove-build-run
remove-build-run:

	$(if $(file_path),@echo "Removing system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory remove file_path=${abs_path}
	@$(MAKE) --no-print-directory build file_path=${abs_path}
	@$(MAKE) --no-print-directory run file_path=${abs_path}

# Removes, rebuilds, and runs generated Docker-Compose file
# Detaches logs from stdout and returns control of terminal
.PHONY: remove-build-run-detached
remove-build-run-detached:

	$(if $(file_path),@echo "Removing system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory remove file_path=${abs_path}
	@$(MAKE) --no-print-directory build file_path=${abs_path}
	@$(MAKE) --no-print-directory run-detached file_path=${abs_path}

# Restarts all containers from generated Docker-Compose file
# Use this command to rebuild code if you have containers that have locally bound code
.PHONY: restart
restart:

	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_RESTART_COMMAND)

# Prints logs from all containers to stdout and follows current logs
.PHONY: logs
logs:

	$(if $(file_path),@echo "Printing logs from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path}  | $(COMPOSE_LOGS_COMMAND)

# Prints only the last n lines from the logs from all containers to stdout and follows current logs
.PHONY: logs-tail
logs-tail:

	$(if $(file_path),@echo "Printing logs from $(file_path)",$(error file_path variable required))
	$(if $(number),,$(error number variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path}  | $(COMPOSE_LOGS_COMMAND) --tail ${number}

# Return container names based off of passed filter.
# Acceptable filters are:
#		heater-shaker-module
#		magnetic-module
#		thermocycler-module
#		temperature-module
#		emulator-proxy
#		smoothie
#		can-server
#		ot3-gantry-x
#		ot3-gantry-y
#		ot3-head
#		ot3-pipettes
#		modules
#		firmware
#		robot-server
#		all
.PHONY: load-container-names
load-container-names:

	$(if $(file_path),,$(error file_path variable required))
	$(if $(filter),,$(error filter variable required))
	@(cd ./emulation_system && pipenv run python main.py load-container-names "${abs_path}" "${filter}")

###########################################
########## OT3 Specific Commands ##########
###########################################

# Run can communication script against can_server
.PHONY: can-comm
can-comm:

	$(if $(file_path),,$(error file_path variable required))
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="can-server" \
		| xargs -o -I{} docker exec -it {} python3 -m opentrons_hardware.scripts.can_comm --interface opentrons_sock


# Runs can monitor script against can_server
.PHONY: can-mon
can-mon:

	$(if $(file_path),,$(error file_path variable required))
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="can-server" \
		| xargs -o -I{} docker exec -it {} python3 -m opentrons_hardware.scripts.can_mon --interface opentrons_sock

###########################################
############### CI Commands ###############
###########################################

# Verifies that all source-types of configuration file are `remote`
.PHONY: check-remote-only
check-remote-only:

	$(if $(file_path),,$(error file_path variable required))
	@$(subst $(SUB), ${abs_path}, $(REMOTE_ONLY_EMULATION_SYSTEM_CMD)) > /dev/null
	@echo "All services are remote"

# Runs generate_compose_file for all configuration files in samples
.PHONY: test-samples
test-samples:

	@./scripts/makefile/helper_scripts/test_samples.sh

# Pushes image bases to Github Container Registry
.PHONY: push-docker-image-bases
push-docker-image-bases:
	@(cd ./docker && ./build_bases.sh)

###########################################
######## emulation_system Commands ########
###########################################

# Setup emulation_system project
.PHONY: setup
setup:

	$(pipenv) sync $(pipenv_opts)
	$(pipenv) run pip freeze
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) setup


# Clean emulation_system project
.PHONY: clean
clean:

	$(clean_cmd)
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) clean


# Clean emulation_system project
.PHONY: teardown
teardown:

	$(pipenv) --rm
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) teardown


# Confirm there are no formatting errors against Markdown files
# Run linting against emulation_system (mypy, isort, black, flake8)
.PHONY: lint
lint:

	$(python) -m mdformat --check .
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) lint


# Run formatting against Markdown files
# Run formatting against emulation_system (isort, black)
.PHONY: format
format:
	$(python) -m mdformat .
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) format


# Run all pytests in emulation_system project
.PHONY: test
test:

	$(MAKE) -C $(EMULATION_SYSTEM_DIR) test
