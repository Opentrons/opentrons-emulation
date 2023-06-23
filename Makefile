EMULATION_SYSTEM_DIR := emulation_system
DOCKER_COMPOSE_EXECUTABLE := docker-compose
ABS_PATH := $(realpath ${file_path})

EMULATION_SYSTEM_CMD = (cd ./${EMULATION_SYSTEM_DIR} && poetry run python main.py emulation-system ${DEV} ${ABS_PATH} - ${REMOTE_ONLY}) | tee docker-compose.yaml
COMPOSE_RUN_COMMAND = DOCKER_BUILDKIT=1 ${DOCKER_COMPOSE_EXECUTABLE} up --remove-orphans ${RUN_DETACHED_OPTION}
COMPOSE_KILL_COMMAND = ${DOCKER_COMPOSE_EXECUTABLE} kill
COMPOSE_START_COMMAND = ${DOCKER_COMPOSE_EXECUTABLE} start
COMPOSE_STOP_COMMAND = ${DOCKER_COMPOSE_EXECUTABLE} stop
COMPOSE_REMOVE_COMMAND = ${DOCKER_COMPOSE_EXECUTABLE} rm --force && docker volume prune -f
COMPOSE_LOGS_COMMAND = ${DOCKER_COMPOSE_EXECUTABLE} logs -f
COMPOSE_RESTART_COMMAND = ${DOCKER_COMPOSE_EXECUTABLE} restart --timeout 1
BUILD_COMMAND = docker buildx bake --load ${BAKE_PROGRESS} ${BAKE_CACHE}


.PHONY: check-file-path
check-file-path:
	$(if $(file_path),,$(error file_path variable required))


.PHONY: emulation-system
emulation-system: check-file-path remove build run-detached refresh-dev start-executables

#####################################################
############# Generating Compose Files ##############
#####################################################
.PHONY: generate-compose-file
generate-compose-file: check-file-path
generate-compose-file:
	@$(EMULATION_SYSTEM_CMD)
	
.PHONY: create-dev-dockerfile
create-dev-dockerfile:
	@./scripts/docker_convenience_scripts/create_dev_dockerfile.sh

.PHONY: dev-generate-compose-file
dev-generate-compose-file: DEV := --dev
dev-generate-compose-file: create-dev-dockerfile
dev-generate-compose-file: generate-compose-file


#####################################################
############## Building Docker Images ###############
#####################################################
.PHONY: build
build: generate-compose-file 
	@$(BUILD_COMMAND)

.PHONY: build-print
build-print: BAKE_PROGRESS := --progress plain
build-print: build

.PHONY: build-no-cache
build-no-cache: BAKE_CACHE := --no-cache
build-no-cache: build

.PHONY: build-print-no-cache
build-print-no-cache: BAKE_PROGRESS := --progress plain
build-print-no-cache: BAKE_CACHE := --no-cache
build-print-no-cache: build

.PHONY: dev-build
dev-build: dev-generate-compose-file
	@$(BUILD_COMMAND)

.PHONY: dev-build-print
dev-build-print: BAKE_PROGRESS := --progress plain
dev-build-print: dev-build


.PHONY: dev-build-no-cache
dev-build-no-cache: BAKE_CACHE := --no-cache
dev-build-no-cache: dev-build

.PHONY: dev-build-print-no-cache
dev-build-print-no-cache: BAKE_PROGRESS := --progress plain
dev-build-print-no-cache: BAKE_CACHE := --no-cache
dev-build-print-no-cache: dev-build


#####################################################
################ Running Emulation ##################
#####################################################
.PHONY: run
run: generate-compose-file
	@$(COMPOSE_RUN_COMMAND)

.PHONY: run-detached
run-detached: RUN_DETACHED_OPTION := -d
run-detached: run

.PHONY: dev-run
dev-run:  dev-generate-compose-file run

.PHONY: dev-run-detached
dev-run-detached: RUN_DETACHED_OPTION := -d
dev-run-detached: dev-run

#####################################################
############## Controlling Emulation ################
#####################################################
.PHONY: start
start: generate-compose-file
	@$(COMPOSE_START_COMMAND)

.PHONY: stop
stop: generate-compose-file
	@$(COMPOSE_STOP_COMMAND)

.PHONY: restart
restart: generate-compose-file
	@$(COMPOSE_RESTART_COMMAND)

.PHONY: remove
remove: generate-compose-file
	$(COMPOSE_KILL_COMMAND)
	$(COMPOSE_REMOVE_COMMAND)

#####################################################
##################### Logging #######################
#####################################################
.PHONY: logs
logs: generate-compose-file
	@$(COMPOSE_LOGS_COMMAND)

.PHONY: logs-tail
logs-tail: generate-compose-file
	$(if $(number),,$(error number variable required))
	@$(COMPOSE_LOGS_COMMAND) --tail ${number}

#####################################################
############### Combination Commands ################
#####################################################
.PHONY: remove-build-run
remove-build-run: remove build run

.PHONY: remove-build-run-detached
remove-build-run-detached: remove build run-detached

###########################################
######### OT-3 Specific Commands ##########
###########################################
.PHONY: can-comm
can-comm: check-file-path
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${ABS_PATH}" \
		filter="can-server" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -it {} monorepo_python -m opentrons_hardware.scripts.can_comm --interface opentrons_sock

.PHONY: can-mon
can-mon: check-file-path
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${ABS_PATH}" \
		filter="can-server" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -it {} monorepo_python -m opentrons_hardware.scripts.can_mon --interface opentrons_sock

.PHONY: refresh-dev
refresh-dev: check-file-path
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${ABS_PATH}" \
		filter="source-builders" \
		| xargs --max-procs=4 --open-tty --no-run-if-empty --replace={} docker exec -t {} /build.sh

	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${ABS_PATH}" \
		filter="monorepo-containers" \
		| xargs --max-procs=6 --open-tty --no-run-if-empty --replace={} docker exec -t {} bash -c "monorepo_python -m pip install /dist/*"

	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${ABS_PATH}" \
		filter="ot3-state-manager" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -t {} bash -c "state_manager_python -m pip install /state-manager-dist/* /dist/*"

.PHONY: refresh-dev-ci
refresh-dev-ci: check-file-path
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${ABS_PATH}" \
		filter="source-builders" \
		| xargs --max-procs=4 --no-run-if-empty --replace={} docker exec -t {} /build.sh


	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${ABS_PATH}" \
		filter="monorepo-containers" \
		| xargs --max-procs=6 --no-run-if-empty --replace={} docker exec -t {} bash -c "monorepo_python -m pip install /dist/*"

	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${ABS_PATH}" \
		filter="ot3-state-manager" \
		| xargs --no-run-if-empty --replace={} docker exec -t {} bash -c "state_manager_python -m pip install /state-manager-dist/* /dist/*"

.PHONY: start-executables
start-executables: check-file-path

	# Start can-server, state-manager and emulator-proxy in the background

	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${ABS_PATH}" \
		filter="can-server" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -d {} /entrypoint.sh
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${ABS_PATH}" \
		filter="emulator-proxy" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -d {} /entrypoint.sh
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${ABS_PATH}" \
		filter="ot3-state-manager" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -d {} /entrypoint.sh

	# Giving CAN Server and emulator-proxy time to start

	sleep 2

	# Starting firmware and modules in background
		
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${ABS_PATH}" \
		filter="smoothie" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -d {} /entrypoint.sh
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${ABS_PATH}" \
		filter="ot3-firmware" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -d {} /entrypoint.sh
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${ABS_PATH}" \
		filter="modules" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -d {} /entrypoint.sh

	# Starting robot-server in the foreground

	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${ABS_PATH}" \
		filter="robot-server" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -it {} /entrypoint.sh

###########################################
############## Misc Commands ##############
###########################################
.PHONY: load-container-names
load-container-names: check-file-path
	$(if $(filter),,$(error filter variable required))
	@(cd ./emulation_system && poetry run python3 main.py lc "${ABS_PATH}" "${filter}")

.PHONY: check-remote-only
check-remote-only: REMOTE_ONLY := --remote-only
check-remote-only: generate-compose-file

.PHONY: push-docker-image-bases
push-docker-image-bases:
	$(if $(branch_name),,$(error branch_name variable required))
	@(cd ./docker && ./build_bases.sh ${branch_name})

OT2CONFIG ?= ./samples/ot2/ot2_with_all_modules.yaml

.PHONY: ot2
ot2: file_path := "${OT2CONFIG}"
ot2: setup check-remote-only remove-build-run


OT3CONFIG ?= ./samples/ot3/ot3_remote.yaml

.PHONY: ot3
ot3:
	$(MAKE) setup
	$(MAKE) check-remote-only file_path="$(OT3CONFIG)"
	$(MAKE) remove-build-run file_path="$(OT3CONFIG)"

ROBOT_HOST := $(if $(shell python ./scripts/docker_convenience_scripts/in_docker.py),host.docker.internal,localhost)

.PHONY: emulation-check
emulation-check:
	curl -s --location --request GET 'http://$(ROBOT_HOST):31950/modules' --header 'opentrons-version: *' | json_pp -json_opt pretty,canonical

###########################################
#### emulation_system Project Commands ####
###########################################
.PHONY: setup
setup:
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) setup

.PHONY: clean
clean:
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) clean

.PHONY: teardown
teardown:
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) teardown

.PHONY: lint
lint:
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) lint

.PHONY: format
format:
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) format

.PHONY: test
test:
	$(MAKE) -C $(EMULATION_SYSTEM_DIR) test

.PHONY: get-e2e-test-ids
get-e2e-test-ids:
	@$(MAKE) --no-print-directory -C $(EMULATION_SYSTEM_DIR) get-e2e-test-ids

.PHONY: get-e2e-test-path
get-e2e-test-path:
	$(if $(test_id),,$(error test_id variable required))
	@$(MAKE) --no-print-directory -C $(EMULATION_SYSTEM_DIR) get-e2e-test-path test_id=${test_id}

.PHONY: execute-e2e-test
execute-e2e-test:
	$(if $(test_id),,$(error test_id variable required))
	@$(MAKE) --no-print-directory -C $(EMULATION_SYSTEM_DIR) execute-e2e-test test_id=${test_id}
