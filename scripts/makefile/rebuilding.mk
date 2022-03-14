
.PHONY: local-exec-containers
local-exec-containers:
	$(if $(file_path),,$(error file_path variable required))
	$(if $(filter),,$(error filter variable required))
	$(if $(cmd),,$(error cmd variable required))
	$(if $(verbosity),,$(error verbosity variable required))
	@$(MAKE) \
		--no-print-directory \
		local-load-containers \
		file_path="${file_path}" \
		filter="${filter}" \
		| xargs -I{} ./scripts/makefile/helper_scripts/rebuild_and_run_local_containers.sh ${cmd} ${verbosity} {}


.PHONY: local-generic-rebuild
local-generic-rebuild:
	$(if $(file_path),,$(error file_path variable required))
	$(if $(filter),,$(error filter variable required))
	$(if $(verbosity),,$(error verbosity variable required))
	@$(MAKE) \
		--no-print-directory \
		local-exec-containers \
		file_path="${file_path}" \
		filter="${filter}" \
		cmd="stop" \
		verbosity="${verbosity}"
	@$(MAKE) \
		--no-print-directory \
		local-exec-containers \
		file_path="${file_path}" \
		filter="${filter}" \
		cmd="build" \
		verbosity="${verbosity}"
	@$(MAKE) \
		--no-print-directory \
		local-exec-containers \
		file_path="${file_path}" \
		filter="${filter}" \
		cmd="run" \
		verbosity="${verbosity}"

.PHONY: local-rebuild-all
local-rebuild-all:
	$(if $(file_path),,$(error file_path variable required))
	@$(MAKE) \
		--no-print-directory \
		local-generic-rebuild \
		file_path="${file_path}" \
		filter="all" \
		verbosity="loud"

.PHONY: local-rebuild-all-quiet
local-rebuild-all-quiet:
	$(if $(file_path),,$(error file_path variable required))
	@$(MAKE) \
		--no-print-directory \
		local-generic-rebuild \
		file_path="${file_path}" \
		filter="all" \
		verbosity="quiet"

.PHONY: local-rebuild-firmware
local-rebuild-firmware:
	$(if $(file_path),,$(error file_path variable required))
	@$(MAKE) \
		--no-print-directory \
		local-generic-rebuild \
		file_path="${file_path}" \
		filter="firmware" \
		verbosity="loud"

.PHONY: local-rebuild-firmware-quiet
local-rebuild-firmware-quiet:
	$(if $(file_path),,$(error file_path variable required))
	@$(MAKE) \
		--no-print-directory \
		local-generic-rebuild \
		file_path="${file_path}" \
		filter="all" \
		verbosity="quiet"
