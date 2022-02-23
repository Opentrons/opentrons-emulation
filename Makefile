EMULATION_SYSTEM_DIR := emulation_system

SUB = {SUB}

EMULATION_SYSTEM_CMD := (cd ./emulation_system && pipenv run python main.py emulation-system {SUB} -)
REMOTE_ONLY_EMULATION_SYSTEM_CMD := (cd ./emulation_system && pipenv run python main.py emulation-system {SUB} - --remote-only)
COMPOSE_BUILD_COMMAND := docker buildx bake --file tmp-compose.yaml
COMPOSE_RUN_COMMAND := docker-compose -f - up
COMPOSE_KILL_COMMAND := docker-compose -f - kill
COMPOSE_REMOVE_COMMAND := docker-compose -f - rm --force
COMPOSE_LOGS_COMMAND := docker-compose -f - logs -f

.PHONY: em-build-amd64
em-build-amd64:
	# TODO: Remove tmp file creation when Buildx 0.8.0 is released.
	# PR: https://github.com/docker/buildx/milestone/11
	# Ticket: https://github.com/docker/buildx/pull/864
	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	@$(subst $(SUB), $(file_path), $(EMULATION_SYSTEM_CMD)) > tmp-compose.yaml && $(COMPOSE_BUILD_COMMAND)
	@rm tmp-compose.yaml

.PHONY: em-build-arm64
em-build-arm64:
	# TODO: Remove tmp file creation when Buildx 0.8.0 is released.
	# PR: https://github.com/docker/buildx/milestone/11
	# Ticket: https://github.com/docker/buildx/pull/864
	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	@$(subst $(SUB), $(file_path), $(EMULATION_SYSTEM_CMD)) > tmp-compose.yaml && $(COMPOSE_BUILD_COMMAND) --set *.platform=linux/x86_64
	@rm tmp-compose.yaml

.PHONY: em-run
em-run:
	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(subst $(SUB), $(file_path), $(EMULATION_SYSTEM_CMD)) | $(COMPOSE_RUN_COMMAND)


.PHONY: em-run-detached
em-run-detached:
	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	@$(subst $(SUB), $(file_path), $(EMULATION_SYSTEM_CMD)) | $(COMPOSE_RUN_COMMAND) -d


.PHONY: em-remove
em-remove:
	$(if $(file_path),@echo "Removing system from $(file_path)",$(error file_path variable required))
	@$(subst $(SUB), $(file_path), $(EMULATION_SYSTEM_CMD)) | $(COMPOSE_KILL_COMMAND)
	@$(subst $(SUB), $(file_path), $(EMULATION_SYSTEM_CMD)) | $(COMPOSE_REMOVE_COMMAND)


.PHONY: em-logs
em-logs:
	$(if $(file_path),@echo "Printing logs from $(file_path)",$(error file_path variable required))
	@$(subst $(SUB), $(file_path), $(EMULATION_SYSTEM_CMD)) | $(COMPOSE_LOGS_COMMAND)


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

.PHONY: test-samples
test-samples:
	@./scripts/test_samples.sh
