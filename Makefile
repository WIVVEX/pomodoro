.DEFAULT_GOAL := help

HOST ?= 127.0.0.1
PORT ?= 8000


run: ## Run app using uvicorn
	poetry run uvicorn app.main:app --host $(HOST) --port $(PORT) --reload --env-file $(ENV_FILE)

add: ## Install a dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall: ## Uninstall a dependency using poetry
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)

migrate-create: ## Create new file for migration
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply: ## Apply migration
	alembic upgrade head

help: ## Show help messages
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf " %-20s %s\n", $$1, $$2}'