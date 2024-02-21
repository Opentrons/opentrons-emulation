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
