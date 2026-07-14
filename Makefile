.PHONY: run dev db-init db-shell test lint clean help

# Variables
APP_MODULE = src.main:app
HOST ?= 127.0.0.1
PORT ?= 8000

help: ## Afficher cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

run: ## Lancer le serveur en mode production
	uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT)

dev: ## Lancer le serveur en mode développement (reload automatique)
	uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT) --reload

db-init: ## Initialiser la base de données (crée les tables)
	python -c "from src.db.connection import init_db; init_db()"

db-shell: ## Ouvrir un shell SQLite interactif sur la base
	sqlite3 data/compagnon.db

test: ## Lancer les tests
	pytest -v

lint: ## Vérifier le formatage et les imports
	black --check src tests
	isort --check src tests

format: ## Formater le code
	black src tests
	isort src tests

clean: ## Supprimer les fichiers générés
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf .venv dist build *.egg-info
