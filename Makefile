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

.PHONY: verify-pnpm-installed
verify-pnpm-installed:
	@echo "Verifying pnpm is installed..."
	@pnpm --version > /dev/null \
		|| ( \
			echo "\n\npnpm is not installed. Run 'make setup-pnpm' to install it.\n\n" \
			&& exit 1 \
		)
	@echo "pnpm is installed."
	@echo

.PHONY: verify-mosquitto
verify-mosquitto:
	@echo "Verifying mosquitto executable exists..."
	@bin/mosquitto --help | grep "mosquitto version" > /dev/null \
		|| ( \
			echo "\n\nmosquitto executable does not exist. Run 'make build-mosquitto' to build it.\n\n" \
			&& exit 1 \
		)
	@echo "mosquitto executable exists."
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

.PHONY: setup-pnpm
setup-pnpm: verify-asdf-configured
	@echo "Installing pnpm..."
	@npm install -g pnpm
	@echo

.PHONY: setup-dev-dependencies
setup-dev-dependencies: verify-asdf-configured verify-pnpm-installed verify-mosquitto add-mosquitto-to-electron
	@echo "Installing dev dependencies..."
	@pnpm install
	@echo

.PHONY: clean
clean:
	@echo "Cleaning up..."
	@rm -rf node_modules \
		bin \
		dist-electron
	@echo

.PHONY: dev
dev:
	@echo "Starting dev env..."
	@pnpm run dev

.PHONY: build-mosquitto
build-mosquitto:
	@echo "Building mosquitto..."
	@./scripts/build_mosquitto.sh

.PHONY: add-mosquitto-to-electron
add-mosquitto-to-electron:
	@echo "Adding mosquitto to electron..."
	@mkdir -p dist-electron
	@cp bin/mosquitto dist-electron
	@echo

