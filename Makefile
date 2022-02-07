SUB = {SUB}
VAGRANT_CMD := ./opentrons-emulation vm && (cd vagrant && vagrant{SUB})


EMULATION_SYSTEM_CMD := ./opentrons-emulation emulation-system {SUB} -
COMPOSE_BUILD_COMMAND := COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f - build
COMPOSE_RUN_COMMAND := docker-compose -f - up -d
COMPOSE_KILL_COMMAND := docker-compose -f - kill
COMPOSE_REMOVE_COMMAND := docker-compose -f - rm --force

.PHONY: vm-create
vm-create:
	$(eval CMD := up)
	$(subst $(SUB), $(CMD), $(VAGRANT_CMD))

.PHONY: vm-remove
vm-remove:
	$(eval CMD := destroy --force)
	$(subst $(SUB), $(CMD), $(VAGRANT_CMD))

.PHONY: vm-ssh
vm-ssh:
	$(eval CMD := ssh default)
	$(subst $(SUB), $(CMD), $(VAGRANT_CMD))

.PHONY: vm-setup
vm-setup:
	$(eval CMD := ssh default -c '(cd opentrons-emulation/emulation_system && make setup)')
	$(subst $(SUB), $(CMD), $(VAGRANT_CMD))

.PHONY: em-build
em-build:
	$(if $(file_path),@echo "Building system from $(file_path)",$(error file_path variable required))
	$(subst $(SUB), $(file_path), $(EMULATION_SYSTEM_CMD)) | $(COMPOSE_BUILD_COMMAND)

.PHONY: em-run
em-run:
	$(if $(file_path),@echo "Running system from $(file_path)",$(error file_path variable required))
	$(subst $(SUB), $(file_path), $(EMULATION_SYSTEM_CMD)) | $(COMPOSE_RUN_COMMAND)


.PHONY: em-remove
em-remove:
	$(if $(file_path),@echo "Removing system from $(file_path)",$(error file_path variable required))
	$(subst $(SUB), $(file_path), $(EMULATION_SYSTEM_CMD)) | $(COMPOSE_KILL_COMMAND)
	$(subst $(SUB), $(file_path), $(EMULATION_SYSTEM_CMD)) | $(COMPOSE_REMOVE_COMMAND)


.PHONY: generate-compose-file
generate-compose-file:
	$(if $(file_path),,$(error file_path variable required))
	$(subst $(SUB), $(file_path), $(EMULATION_SYSTEM_CMD))


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
