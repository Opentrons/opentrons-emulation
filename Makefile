.PHONY: verify-asdf-installed
verify-asdf-installed:
	@echo "Verifying asdf is installed..."
	@asdf --version > /dev/null \
		|| ( \
			echo "\n\nPlease visit https://asdf-vm.com/guide/getting-started.html#_1-install-dependencies for installation instructions.\n\n" \
			&& exit 1 \
		)
	@echo "asdf is installed."
	@echo
	

.PHONY: verify-asdf-configured
verify-asdf-configured: verify-asdf-installed
	@echo "Verifying asdf is configured..."
	@asdf current | grep -qP "nodejs +\d+.\d+.\d+" \
		|| ( \
			echo "\n\nasdf is not configured. Run 'make setup-asdf' to configure it.\n\n" \
			&& exit 1 \
		)
	@echo "asdf is configured."
	@echo

.PHONY: verify-yarn-installed
verify-yarn-installed:
	@echo "Verifying yarn is installed..."
	@yarn --version > /dev/null \
		|| ( \
			echo "\n\nyarn is not installed. Run 'make setup-yarn' to install it.\n\n" \
			&& exit 1 \
		)
	@echo "yarn is installed."
	@echo

.PHONY: add-asdf-plugins
add-asdf-plugins: verify-asdf-installed
	@echo "Adding nodejs asdf plugin..."
	@asdf plugin-add nodejs
	@echo


.PHONY: setup-asdf
setup-asdf: add-asdf-plugins
	@echo "Installing nodejs..."
	@asdf install
	@echo

.PHONY: teardown-asdf
teardown-asdf:
	@echo "Uninstalling nodejs"
	@asdf plugin remove nodejs
	@echo

.PHONY: setup-yarn
setup-yarn: verify-asdf-configured
	@echo "Installing yarn..."
	@npm install -g yarn@v1
	@echo

.PHONY: setup-frontend
setup-frontend: verify-asdf-configured verify-yarn-installed
	@echo "Installing frontend dependencies..."
	@yarn install
	@echo

.PHONY: setup-dev-dependencies
setup-dev-dependencies: setup-asdf setup-yarn setup-frontend add-mosquitto-sidecar

.PHONY: clean
clean:
	@echo "Cleaning up..."
	@rm -rf $(TAURI_BINARY_DIR) \
		$(TAURI_DIR)/.env \
		$(TAURI_DIR)/out \
		$(TAURI_DIR)/target \
		node_modules \
		bin \
		.next
	@echo

.PHONY: dev
dev:
	@echo "Starting dev env..."
	@cp .dev.env $(TAURI_DIR)/.env
	@yarn tauri dev

.PHONY: build 
build:
	@echo "Building tauri..."
	@yarn tauri build

.PHONY: build-mosquitto
build-mosquitto:
	@echo "Building mosquitto..."
	@./scripts/build_mosquitto.sh

.PHONY: add-mosquitto-sidecar
add-mosquitto-sidecar: build-mosquitto
	@echo "Adding mosquitto sidecar to tauri..."
	@mkdir -p $(TAURI_BINARY_DIR)
	@cp ./bin/mosquitto $(TAURI_BINARY_DIR)/$$(yarn --silent get-sidecar-name ./bin/mosquitto)