"""Point d'entrée FastAPI du Compagnon de jardin.

Lancement : uvicorn src.main:app --reload
"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.config import APP_NAME, APP_VERSION, DEBUG
from src.db.connection import init_db

# Création de l'application
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Système hybride d'accompagnement au potager nourricier",
)

# Templates Jinja2 (SSR + HTMX)
templates_dir: Path = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Fichiers statiques (CSS, JS, manifest PWA)
static_dir: Path = Path(__file__).parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# --- Routes racine ---

@app.get("/")
def index(request: Request):
    """Page d'accueil."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": APP_NAME,
            "app_version": APP_VERSION,
        },
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
    # La base est initialisée manuellement via `make db-init`
    # pour éviter de la recréer à chaque démarrage


# --- Inclusion des modules (au fur et à mesure de leur développement) ---

# Exemple pour le module journal (plus tard) :
# from src.modules.journal.routes import router as journal_router
# app.include_router(journal_router, prefix="/journal", tags=["Journal"])
