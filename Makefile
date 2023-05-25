EMULATION_SYSTEM_DIR := emulation_system

SUB = {SUB}

EMULATION_SYSTEM_CMD := (cd ./emulation_system && poetry run python main.py emulation-system {SUB} -)
DEV_EMULATION_SYSTEM_CMD := (cd ./emulation_system && poetry run python main.py emulation-system --dev {SUB} -)
REMOTE_ONLY_EMULATION_SYSTEM_CMD := (cd ./emulation_system && poetry run python main.py emulation-system {SUB} - --remote-only)
COMPOSE_RUN_COMMAND := DOCKER_BUILDKIT=1 docker-compose -f - up --remove-orphans
COMPOSE_KILL_COMMAND := docker-compose -f - kill
COMPOSE_START_COMMAND := docker-compose -f - start
COMPOSE_STOP_COMMAND := docker-compose -f - stop
COMPOSE_REMOVE_COMMAND := docker-compose -f - rm --force && docker volume prune -f
COMPOSE_LOGS_COMMAND := docker-compose -f - logs -f
COMPOSE_RESTART_COMMAND := docker-compose -f - restart --timeout 1
BUILD_COMMAND := docker buildx bake --load --file ~/tmp-compose.yaml

abs_path := $(realpath ${file_path})

#####################################################
############# Generating Compose Files ##############
#####################################################
.PHONY: generate-compose-file
generate-compose-file:
	$(if $(file_path),,$(error file_path variable required))
	@$(subst $(SUB), ${abs_path}, $(EMULATION_SYSTEM_CMD))

.PHONY: dev-generate-compose-file
dev-generate-compose-file:
	$(if $(file_path),,$(error file_path variable required))
	@./scripts/docker_convenience_scripts/create_dev_dockerfile.sh
	@$(subst $(SUB), ${abs_path}, $(DEV_EMULATION_SYSTEM_CMD))


#####################################################
############## Building Docker Images ###############
#####################################################
.PHONY: build
build:
	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory --quiet generate-compose-file file_path=${abs_path} > ~/tmp-compose.yaml
	@$(BUILD_COMMAND)
	@rm ~/tmp-compose.yaml

.PHONY: build-print
build-print:
	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory --quiet generate-compose-file file_path=${abs_path} > ~/tmp-compose.yaml
	@$(BUILD_COMMAND) --progress plain
	@rm ~/tmp-compose.yaml

.PHONY: build-no-cache
build-no-cache:
	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory --quiet generate-compose-file file_path=${abs_path} > ~/tmp-compose.yaml
	@$(BUILD_COMMAND) --no-cache
	@rm ~/tmp-compose.yaml

.PHONY: build-print-no-cache
build-print-no-cache:
	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory --quiet generate-compose-file file_path=${abs_path} > ~/tmp-compose.yaml
	@$(BUILD_COMMAND) --progress plain --no-cache
	@rm ~/tmp-compose.yaml

.PHONY: dev-build
dev-build:
	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory --quiet dev-generate-compose-file file_path=${abs_path} > ~/tmp-compose.yaml
	@$(BUILD_COMMAND)
	@rm ~/tmp-compose.yaml

.PHONY: dev-build-print
dev-build-print:
	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory --quiet dev-generate-compose-file file_path=${abs_path} > ~/tmp-compose.yaml
	@$(BUILD_COMMAND) --progress plain
	@rm ~/tmp-compose.yaml

.PHONY: dev-build-no-cache
dev-build-no-cache:
	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory --quiet dev-generate-compose-file file_path=${abs_path} > ~/tmp-compose.yaml
	@$(BUILD_COMMAND) --no-cache
	@rm ~/tmp-compose.yaml

.PHONY: dev-build-print-no-cache
dev-build-print-no-cache:
	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory --quiet dev-generate-compose-file file_path=${abs_path} > ~/tmp-compose.yaml
	@$(BUILD_COMMAND) --progress plain --no-cache
	@rm ~/tmp-compose.yaml


#####################################################
################ Running Emulation ##################
#####################################################
.PHONY: run
run:
	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_RUN_COMMAND)

.PHONY: run-detached
run-detached:
	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_RUN_COMMAND) -d

.PHONY: dev-run
dev-run:
	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory dev-generate-compose-file file_path=${abs_path} | $(COMPOSE_RUN_COMMAND)

.PHONY: dev-run-detached
dev-run-detached:
	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory dev-generate-compose-file file_path=${abs_path} | $(COMPOSE_RUN_COMMAND) -d

#####################################################
############## Controlling Emulation ################
#####################################################
.PHONY: start
start:
	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_START_COMMAND)

.PHONY: stop
stop:
	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_STOP_COMMAND)

.PHONY: restart
restart:
	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_RESTART_COMMAND)

.PHONY: remove
remove:
	$(if $(file_path),@echo "Removing system from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_KILL_COMMAND)
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path} | $(COMPOSE_REMOVE_COMMAND)

#####################################################
##################### Logging #######################
#####################################################
.PHONY: logs
logs:
	$(if $(file_path),@echo "Printing logs from $(file_path)",$(error file_path variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path}  | $(COMPOSE_LOGS_COMMAND)

.PHONY: logs-tail
logs-tail:
	$(if $(file_path),@echo "Printing logs from $(file_path)",$(error file_path variable required))
	$(if $(number),,$(error number variable required))
	@$(MAKE) --no-print-directory generate-compose-file file_path=${abs_path}  | $(COMPOSE_LOGS_COMMAND) --tail ${number}

#####################################################
############### Combination Commands ################
#####################################################
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

###########################################
######### OT-3 Specific Commands ##########
###########################################
.PHONY: can-comm
can-comm:
	$(if $(file_path),,$(error file_path variable required))
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="can-server" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -it {} monorepo_python -m opentrons_hardware.scripts.can_comm --interface opentrons_sock

.PHONY: can-mon
can-mon:
	$(if $(file_path),,$(error file_path variable required))
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="can-server" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -it {} monorepo_python -m opentrons_hardware.scripts.can_mon --interface opentrons_sock

.PHONY: refresh-dev
refresh-dev:
	$(if $(file_path),,$(error file_path variable required))
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="source-builders" \
		| xargs --max-procs=4 --open-tty --no-run-if-empty --replace={} docker exec -t {} /build.sh

	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="monorepo-containers" \
		| xargs --max-procs=6 --open-tty --no-run-if-empty --replace={} docker exec -t {} bash -c "monorepo_python -m pip install /dist/*"

	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="ot3-state-manager" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -t {} bash -c "state_manager_python -m pip install /state-manager-dist/* /dist/*"

.PHONY: refresh-dev-ci
refresh-dev-ci:
	$(if $(file_path),,$(error file_path variable required))
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="source-builders" \
		| xargs --max-procs=4 --no-run-if-empty --replace={} docker exec -t {} /build.sh


	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="monorepo-containers" \
		| xargs --max-procs=6 --no-run-if-empty --replace={} docker exec -t {} bash -c "monorepo_python -m pip install /dist/*"

	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="ot3-state-manager" \
		| xargs --no-run-if-empty --replace={} docker exec -t {} bash -c "state_manager_python -m pip install /state-manager-dist/* /dist/*"

.PHONY: start-executables
start-executables:
	$(if $(file_path),,$(error file_path variable required))
	# Start can-server and emulator-proxy in the background
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="can-server" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -d {} /entrypoint.sh
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="emulator-proxy" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -d {} /entrypoint.sh
	
	# Giving CAN Server and emulator-proxy time to start

	sleep 2

	# Starting firmware and modules in background
		
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="smoothie" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -d {} /entrypoint.sh

	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="ot3-firmware" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -d {} /entrypoint.sh
		
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="modules" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -d {} /entrypoint.sh

	# # Starting robot-server in the foreground
	@$(MAKE) \
		--no-print-directory \
		load-container-names \
		file_path="${abs_path}" \
		filter="robot-server" \
		| xargs --open-tty --no-run-if-empty --replace={} docker exec -it {} /entrypoint.sh

###########################################
############## Misc Commands ##############
###########################################
.PHONY: load-container-names
load-container-names:
	$(if $(file_path),,$(error file_path variable required))
	$(if $(filter),,$(error filter variable required))
	@(cd ./emulation_system && poetry run python3 main.py lc "${abs_path}" "${filter}")

.PHONY: check-remote-only
check-remote-only:
	$(if $(file_path),,$(error file_path variable required))
	@$(subst $(SUB), ${abs_path}, $(REMOTE_ONLY_EMULATION_SYSTEM_CMD)) > /dev/null
	@echo "All services are remote"

.PHONY: push-docker-image-bases
push-docker-image-bases:
	$(if $(branch_name),,$(error branch_name variable required))
	@(cd ./docker && ./build_bases.sh ${branch_name})

OT2CONFIG ?= ./samples/ot2/ot2_with_all_modules.yaml

.PHONY: ot2
ot2:
	$(MAKE) setup
	$(MAKE) check-remote-only file_path="$(OT2CONFIG)"
	$(MAKE) remove-build-run file_path="$(OT2CONFIG)"

FLEXCONFIG ?= ./samples/ot3/ot3_remote.yaml

.PHONY: flex
flex:
	$(MAKE) setup
	$(MAKE) check-remote-only file_path="$(FLEXCONFIG)"
	$(MAKE) remove-build-run file_path="$(FLEXCONFIG)"

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
