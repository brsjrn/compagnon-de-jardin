"""Configuration centralisée de l'application.

Charge les variables depuis .env (python-dotenv) et expose
les constantes utilisées par tous les modules.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Charger .env à la racine du projet
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Chemins
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = PROJECT_ROOT / "data"
DB_PATH: Path = DATA_DIR / "compagnon.db"
SCHEMA_PATH: Path = PROJECT_ROOT / "src" / "db" / "schema.sql"

# Serveur
HOST: str = os.getenv("HOST", "127.0.0.1")
PORT: int = int(os.getenv("PORT", "8000"))
DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

# Deepseek API (compatible OpenAI SDK)
DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL: str = os.getenv(
    "DEEPSEEK_BASE_URL", "https://api.deepseek.com"
)
DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# Météo (API open data, ex: Open-Meteo, pas de clé requise)
METEO_API_URL: str = os.getenv(
    "METEO_API_URL", "https://api.open-meteo.com/v1/forecast"
)

# Application
APP_NAME: str = "Compagnon de jardin"
APP_VERSION: str = "0.1.0"
