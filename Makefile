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
COMPOSE_BUILD_COMMAND := docker buildx bake --file tmp-compose.yaml --progress plain
COMPOSE_RUN_COMMAND := docker-compose -f - up
COMPOSE_KILL_COMMAND := docker-compose -f - kill
COMPOSE_REMOVE_COMMAND := docker-compose -f - rm --force
COMPOSE_LOGS_COMMAND := docker-compose -f - logs -f
COMPOSE_RESTART_COMMAND := docker-compose -f - restart --timeout 1

abs_path := $(realpath ${file_path})

###########################################
####### Emulation Control Commands ########
###########################################

.PHONY: generate-compose-file
generate-compose-file:

	# Generates Docker-Compose file from passed configuration file and outputs it to stdout

	$(if $(file_path),,$(error file_path variable required))
	@$(subst $(SUB), ${abs_path}, $(EMULATION_SYSTEM_CMD))

.PHONY: build
build:

	# Builds generated Docker-Compose file's necessary images using docker buildx
	# Note 1: This repository supports building against `x86_64` and `arm64` type processors
	#
	# Note 2: Docker images should be rebuilt under the following conditions:
	#
	#	If anything changes in your configuration file
	#	If you have an emulator using `remote` source type, `latest` source location, and there has been an update to the main branch of the source repo
	#	If the underlying Dockerfile changes

	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} > ~/tmp-compose.yaml
	./scripts/makefile/helper_scripts/build.sh ~/tmp-compose.yaml
	@rm ~/tmp-compose.yaml

.PHONY: run
run:

	# Creates and starts Docker Containers from generated Docker-Compose file
	# Outputs logs to stdout
	# Stops and removes containers on exit of logs

	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_RUN_COMMAND)

.PHONY: run-detached
run-detached:

	# Creates and starts Docker Containers from generated Docker-Compose file
	# Detaches logs from stdout and returns control of terminal

	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_RUN_COMMAND) -d

.PHONY: remove
remove:

	# Removes containers from generated Docker-Compose file

	$(if $(file_path),@echo "Removing system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_KILL_COMMAND)
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_REMOVE_COMMAND)

.PHONY: remove-build-run
remove-build-run:

	# Removes, rebuilds, and runs generated Docker-Compose file
	# Outputs logs to stdout
	# Stops and removes containers on exit of logs

	$(if $(file_path),@echo "Removing system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory remove file_path=${abs_path}
	@$(MAKE) --no-print-directory build file_path=${abs_path}
	@$(MAKE) --no-print-directory run file_path=${abs_path}

.PHONY: remove-build-run-detached
remove-build-run-detached:

	# Removes, rebuilds, and runs generated Docker-Compose file
	# Detaches logs from stdout and returns control of terminal

	$(if $(file_path),@echo "Removing system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory remove file_path=${abs_path}
	@$(MAKE) --no-print-directory build file_path=${abs_path}
	@$(MAKE) --no-print-directory run-detached file_path=${abs_path}

.PHONY: restart
restart:

	# Restarts all containers from generated Docker-Compose file
	# Use this command to rebuild code if you have containers that have locally bound code

	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_RESTART_COMMAND)

.PHONY: logs
logs:

	# Prints logs from all containers to stdout and follows current logs

	$(if $(file_path),@echo "Printing logs from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path}  | $(COMPOSE_LOGS_COMMAND)

.PHONY: logs-tail
logs-tail:

	# Prints only the last n lines from the logs from all containers to stdout and follows current logs

	$(if $(file_path),@echo "Printing logs from $(file_path)",$(error file_path variable required))
	$(if $(number),,$(error number variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path}  | $(COMPOSE_LOGS_COMMAND) --tail ${number}

.PHONY: load-container-names
load-container-names:

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


	$(if $(file_path),,$(error file_path variable required))
	$(if $(filter),,$(error filter variable required))
	@(cd ./emulation_system && pipenv run python main.py load-container-names "${abs_path}" "${filter}")

###########################################
########## OT3 Specific Commands ##########
###########################################

.PHONY: can-comm
can-comm:

	# Run can communication script against can_server

	$(if $(file_path),,$(error file_path variable required))
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="can-server" \
		| xargs -o -I{} docker exec -it {} python3 -m opentrons_hardware.scripts.can_comm --interface opentrons_sock


.PHONY: can-mon
can-mon:

	# Runs can monitor script against can_server

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

.PHONY: check-remote-only
check-remote-only:

	# Verifies that all source-types of configuration file are `remote`

	$(if $(file_path),,$(error file_path variable required))
	@$(subst $(SUB), ${abs_path}, $(REMOTE_ONLY_EMULATION_SYSTEM_CMD)) > /dev/null
	@echo "All services are remote"

.PHONY: test-samples
test-samples:

	# Runs generate_compose_file for all configuration files in samples

	@./scripts/makefile/helper_scripts/test_samples.sh

###########################################
######## emulation_system Commands ########
###########################################

.PHONY: setup
setup:

	# Setup emulation_system project

	$(pipenv) sync $(pipenv_opts)
	$(pipenv) run pip freeze
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) setup


.PHONY: clean
clean:

	# Clean emulation_system project

	$(clean_cmd)
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) clean


.PHONY: teardown
teardown:

	# Teardown emulation_system project

	$(pipenv) --rm
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) teardown


.PHONY: lint
lint:

	# Confirm there are no formatting errors against Markdown files
	# Run linting against emulation_system (mypy, isort, black, flake8)

	$(python) -m mdformat --check .
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) lint


.PHONY: format
format:
	# Run formatting against Markdown files
	# Run formatting against emulation_system (isort, black)
	$(python) -m mdformat .
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) format


.PHONY: test
test:

	# Run all pytests in emulation_system project

	$(MAKE) -C $(EMULATION_SYSTEM_DIR) test
