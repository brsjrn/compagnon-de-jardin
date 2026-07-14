"""Point d'entrée FastAPI du Compagnon de jardin.

Lancement : uvicorn src.main:app --reload
"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from src.config import APP_NAME, APP_VERSION, DEBUG
from src.templating import templates

# Création de l'application
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Système hybride d'accompagnement au potager nourricier",
)

# Fichiers statiques (CSS, JS, manifest PWA)
static_dir: Path = Path(__file__).parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# --- Routes racine ---

@app.get("/")
def index(request: Request):
    """Page d'accueil."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.get("/health")
def health():
    """Endpoint de santé (monitoring)."""
    return {"status": "ok", "version": APP_VERSION}


# --- Événements de cycle de vie ---

@app.on_event("startup")
def startup_event():
    """Actions au démarrage du serveur."""
    print(f"🌱 {APP_NAME} v{APP_VERSION}")
    if DEBUG:
        print("⚠️  Mode DEBUG activé")


# --- Modules ---

import importlib

# Module 01 — Journal
journal_routes = importlib.import_module("src.modules.01_journal.routes")
app.include_router(journal_routes.router)

# Module 02 — Connaissances
connaissances_routes = importlib.import_module("src.modules.02_connaissances.routes")
app.include_router(connaissances_routes.router)

# Module 03 — Planification
planification_routes = importlib.import_module("src.modules.03_planification.routes")
app.include_router(planification_routes.router)
