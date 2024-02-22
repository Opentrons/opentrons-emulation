TAURI_BINARY_DIR = ./apps/frontend/src-tauri/binaries

.PHONY: check-asdf
check-asdf:
	@echo "Checking if asdf is installed..."
	@./scripts/check_asdf.sh
	@echo
	

.PHONY: add-asdf-plugins
add-asdf-plugins: check-asdf
	@echo "Adding nodejs asdf plugin..."
	@asdf plugin-add nodejs
	@echo

	@echo "Adding rust asdf plugin..."
	@asdf plugin-add rust
	@echo

.PHONY: setup-asdf
setup-asdf: add-asdf-plugins
	@echo "Installing nodejs and rust..."
	@asdf install
	@echo

.PHONY: setup-frontend
setup-frontend: setup-asdf
	@echo "Installing frontend dependencies..."
	@(cd apps/frontend && yarn install)
	@echo

.PHONY: setup
setup: setup-frontend

.PHONY: dev-frontend
dev-frontend:
	@echo "Starting frontend dev..."
	@(cd apps/frontend && yarn tauri dev)

.PHONY: build-mosquitto
build-mosquitto:
	@echo "Building mosquitto..."
	@./scripts/build_mosquitto.sh

.PHONY: add-mosquitto-sidecar
add-mosquitto-sidecar: build-mosquitto
	@echo "Adding mosquitto sidecar to tauri..."
	@mkdir -p $(TAURI_BINARY_DIR)
	@cp ./bin/mosquitto $(TAURI_BINARY_DIR)/$$(cd apps/frontend && yarn --silent get-sidecar-name ../../bin/mosquitto)