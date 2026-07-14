"""Module partagé pour les templates Jinja2.

Évite les imports circulaires entre main.py et les modules.
"""

from pathlib import Path

from fastapi.templating import Jinja2Templates

from src.config import APP_NAME, APP_VERSION

# Répertoire des templates
TEMPLATES_DIR: Path = Path(__file__).parent / "templates"

# Instance unique des templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
templates.env.globals["app_name"] = APP_NAME
templates.env.globals["app_version"] = APP_VERSION
