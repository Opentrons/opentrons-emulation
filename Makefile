EMULATION_SYSTEM_DIR := emulation_system
DOCKER_EXECUTABLE := docker
DOCKER_COMPOSE_EXECUTABLE := docker-compose

ABS_PATH = $(realpath ${file_path})
LOAD_CONTAINER_NAMES_CMD = (cd ./emulation_system && poetry run python3 main.py lc ${ABS_PATH} $(1))

XARGS_COMMAND = xargs $(1) --max-procs $(2) --no-run-if-empty --replace={}
XARGS_W_TTY = $(call XARGS_COMMAND,--open-tty,$(1))
XARGS_WO_TTY = $(call XARGS_COMMAND,,$(1))

DOCKER_EXEC = ${DOCKER_EXECUTABLE} exec $(1) {}
DOCKER_EXEC_DETACHED = $(call DOCKER_EXEC,-d)
DOCKER_EXEC_INTERACTIVE = $(call DOCKER_EXEC,-it)
DOCKER_EXEC_TTY_ONLY = $(call DOCKER_EXEC,-t)

.PHONY: check-file-path
check-file-path: $(if $(file_path),,$(error file_path variable required))

.PHONY: emulation-system
emulation-system: check-file-path remove build run-detached refresh-dev start-executables

#####################################################
############# Generating Compose Files ##############
#####################################################
.PHONY: generate-compose-file
generate-compose-file: check-file-path
generate-compose-file:
	@(\
		cd ./${EMULATION_SYSTEM_DIR} &&\
		poetry run python main.py emulation-system ${DEV} ${ABS_PATH} - ${REMOTE_ONLY}\
	) | tee docker-compose.yaml
	
	
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
	@${DOCKER_EXECUTABLE} buildx bake --load ${BAKE_PROGRESS} ${BAKE_CACHE}

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
dev-build: build

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
	@DOCKER_BUILDKIT=1 ${DOCKER_COMPOSE_EXECUTABLE} up --remove-orphans ${RUN_DETACHED_OPTION}

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
	@${DOCKER_COMPOSE_EXECUTABLE} start

.PHONY: stop
stop: generate-compose-file
	@${DOCKER_COMPOSE_EXECUTABLE} stop

.PHONY: restart
restart: generate-compose-file
	@${DOCKER_COMPOSE_EXECUTABLE} restart --timeout 1

.PHONY: remove
remove: generate-compose-file
	@${DOCKER_COMPOSE_EXECUTABLE} kill
	@${DOCKER_COMPOSE_EXECUTABLE} rm --force && ${DOCKER_EXECUTABLE} volume prune -f

#####################################################
##################### Logging #######################
#####################################################
.PHONY: logs
logs: NUMBER := 200
logs: generate-compose-file
	${DOCKER_COMPOSE_EXECUTABLE} logs -f --tail ${NUMBER}

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
	@$(call LOAD_CONTAINER_NAMES_CMD,can-server) | $(call XARGS_W_TTY,1) $(DOCKER_EXEC_INTERACTIVE) monorepo_python -m opentrons_hardware.scripts.can_comm --interface opentrons_sock

.PHONY: can-mon
can-mon: check-file-path
	@$(call LOAD_CONTAINER_NAMES_CMD,can-server) | $(call XARGS_W_TTY,1) $(DOCKER_EXEC_INTERACTIVE) monorepo_python -m opentrons_hardware.scripts.can_mon --interface opentrons_sock

.PHONY: refresh-dev-ci
refresh-dev-ci: XARGS_CMD_TO_RUN := XARGS_WO_TTY
refresh-dev-ci: check-file-path

	$(call LOAD_CONTAINER_NAMES_CMD,source-builders) | \
	$(call ${XARGS_CMD_TO_RUN},4) \
	$(DOCKER_EXEC_TTY_ONLY) \
	/build.sh

	$(call LOAD_CONTAINER_NAMES_CMD,monorepo-containers) | \
	$(call ${XARGS_CMD_TO_RUN},6) \
	$(DOCKER_EXEC_TTY_ONLY) \
	bash -c "monorepo_python -m pip install /dist/*"

	$(call LOAD_CONTAINER_NAMES_CMD,ot3-state-manager) | \
	$(call ${XARGS_CMD_TO_RUN},1) \
	$(DOCKER_EXEC_TTY_ONLY) \


.PHONY: refresh-dev
refresh-dev: XARGS_CMD_TO_RUN := XARGS_W_TTY
refresh-dev: refresh-dev-ci

.PHONY: start-executables
start-executables: TTY := --open-tty
start-executables: check-file-path

	# Start can-server, state-manager and emulator-proxy in the background
	@$(\
		foreach container,\
		can-server emulator-proxy ot3-state-manager,\
		$(call LOAD_CONTAINER_NAMES_CMD,$(container)) | $(XARGS_COMMAND) $(DOCKER_EXEC_DETACHED) /entrypoint.sh;\
	)

	# Giving CAN Server and emulator-proxy time to start

	sleep 2

	# Starting firmware and modules in background
	@$(\
		foreach container,\
		smoothie ot3-firmware modules,$(call LOAD_CONTAINER_NAMES_CMD,$(container)) | $(XARGS_COMMAND) $(DOCKER_EXEC_DETACHED) /entrypoint.sh;\
	)


	# Starting robot-server in foreground
	@$(call LOAD_CONTAINER_NAMES_CMD,robot-server) | $(XARGS_COMMAND) $(DOCKER_EXEC_INTERACTIVE) /entrypoint.sh

###########################################
############## Misc Commands ##############
###########################################
.PHONY: load-container-names
load-container-names: check-file-path check-filter
	$(call LOAD_CONTAINER_NAMES_CMD,${filter})

.PHONY: check-remote-only
check-remote-only: REMOTE_ONLY := --remote-only
check-remote-only: generate-compose-file

.PHONY: push-docker-image-bases
push-docker-image-bases:
	$(if $(branch_name),,$(error branch_name variable required))
	@(cd ./docker && ./build_bases.sh ${branch_name})

OT2CONFIG ?= ./samples/ot2/ot2_with_all_modules.yaml

.PHONY: ot2
ot2: file_path := ${OT2CONFIG}
ot2: setup check-remote-only remove-build-run


OT3CONFIG ?= ./samples/ot3/ot3_remote.yaml

.PHONY: ot3
ot3: file_path := ${OT3CONFIG}
ot3: setup check-remote-only remove-build-run

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
