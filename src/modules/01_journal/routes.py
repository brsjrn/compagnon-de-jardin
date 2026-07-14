"""Routes du module 01 — Journal de culture.

Endpoints REST + HTMX pour la gestion des interventions,
observations et parcelles.
"""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

import importlib as _importlib

from src.db.connection import execute, query
from src.templating import templates

_models = _importlib.import_module("src.modules.01_journal.models")
TYPES_INTERVENTION = _models.TYPES_INTERVENTION
TYPES_OBSERVATION = _models.TYPES_OBSERVATION

router = APIRouter(prefix="/journal", tags=["Journal"])


# ═══════════════════════════════════════════════════════════════
# Page principale du journal
# ═══════════════════════════════════════════════════════════════

@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
def journal_index(request: Request):
    """Page principale du journal avec les trois onglets."""
    return templates.TemplateResponse(
        request=request,
        name="journal/index.html",
    )


# ═══════════════════════════════════════════════════════════════
# HTMX — Chargement des listes (chaque onglet)
# ═══════════════════════════════════════════════════════════════

@router.get("/liste/interventions", response_class=HTMLResponse)
def liste_interventions(
    request: Request,
    page: int = 1,
    type_filter: Optional[str] = None,
    parcelle_id: Optional[int] = None,
):
    """Retourne le fragment HTML de la liste des interventions."""
    limit = 20
    offset = (page - 1) * limit

    conditions = []
    params: list = []

    if type_filter:
        conditions.append("i.type = ?")
        params.append(type_filter)
    if parcelle_id:
        conditions.append("i.parcelle_id = ?")
        params.append(parcelle_id)

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    rows = query(
        f"""SELECT i.id, i.date_intervention, i.type, i.description,
                   i.duree_minutes, i.parcelle_id, i.created_at,
                   p.nom AS parcelle_nom
            FROM interventions i
            LEFT JOIN parcelles p ON i.parcelle_id = p.id
            WHERE {where_clause}
            ORDER BY i.date_intervention DESC, i.created_at DESC
            LIMIT ? OFFSET ?""",
        params + [limit, offset],
    )

    # Récupérer les parcelles pour les filtres
    parcelles = query("SELECT id, nom FROM parcelles ORDER BY nom")

    return templates.TemplateResponse(
        request=request,
        name="journal/partials/intervention_list.html",
        context={
            "interventions": [dict(r) for r in rows],
            "parcelles": [dict(p) for p in parcelles],
            "type_filter": type_filter or "",
            "parcelle_filter": parcelle_id or 0,
            "page": page,
            "has_more": len(rows) == limit,
        },
    )


@router.get("/liste/observations", response_class=HTMLResponse)
def liste_observations(
    request: Request,
    page: int = 1,
    type_filter: Optional[str] = None,
):
    """Retourne le fragment HTML de la liste des observations."""
    limit = 20
    offset = (page - 1) * limit

    conditions = []
    params: list = []

    if type_filter:
        conditions.append("o.type = ?")
        params.append(type_filter)

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    rows = query(
        f"""SELECT o.id, o.date_observation, o.type, o.description,
                   o.parcelle_id, o.chemin_fichier, o.created_at,
                   p.nom AS parcelle_nom
            FROM observations o
            LEFT JOIN parcelles p ON o.parcelle_id = p.id
            WHERE {where_clause}
            ORDER BY o.date_observation DESC, o.created_at DESC
            LIMIT ? OFFSET ?""",
        params + [limit, offset],
    )

    parcelles = query("SELECT id, nom FROM parcelles ORDER BY nom")

    return templates.TemplateResponse(
        request=request,
        name="journal/partials/observation_list.html",
        context={
            "observations": [dict(r) for r in rows],
            "parcelles": [dict(p) for p in parcelles],
            "type_filter": type_filter or "",
            "page": page,
            "has_more": len(rows) == limit,
        },
    )


@router.get("/liste/parcelles", response_class=HTMLResponse)
def liste_parcelles(request: Request):
    """Retourne le fragment HTML de la liste des parcelles."""
    rows = query("SELECT * FROM parcelles ORDER BY nom")
    return templates.TemplateResponse(
        request=request,
        name="journal/partials/parcelle_list.html",
        context={"parcelles": [dict(r) for r in rows]},
    )


# ═══════════════════════════════════════════════════════════════
# HTMX — Formulaires (affichage)
# ═══════════════════════════════════════════════════════════════

@router.get("/form/intervention", response_class=HTMLResponse)
def form_intervention(request: Request, parcelle_id: Optional[int] = None):
    """Retourne le formulaire vierge pour une intervention."""
    parcelles = query("SELECT id, nom FROM parcelles ORDER BY nom")
    return templates.TemplateResponse(
        request=request,
        name="journal/partials/intervention_form.html",
        context={
            "today": date.today().isoformat(),
            "types": TYPES_INTERVENTION,
            "parcelles": [dict(p) for p in parcelles],
            "preselected_parcelle": parcelle_id or 0,
        },
    )


@router.get("/form/observation", response_class=HTMLResponse)
def form_observation(request: Request, parcelle_id: Optional[int] = None):
    """Retourne le formulaire vierge pour une observation."""
    parcelles = query("SELECT id, nom FROM parcelles ORDER BY nom")
    return templates.TemplateResponse(
        request=request,
        name="journal/partials/observation_form.html",
        context={
            "today": date.today().isoformat(),
            "types": TYPES_OBSERVATION,
            "parcelles": [dict(p) for p in parcelles],
            "preselected_parcelle": parcelle_id or 0,
        },
    )


@router.get("/form/parcelle", response_class=HTMLResponse)
def form_parcelle(request: Request):
    """Retourne le formulaire vierge pour une parcelle."""
    return templates.TemplateResponse(
        request=request,
        name="journal/partials/parcelle_form.html",
    )


# ═══════════════════════════════════════════════════════════════
# CRUD — Interventions
# ═══════════════════════════════════════════════════════════════

@router.post("/interventions", response_class=HTMLResponse)
def creer_intervention(
    request: Request,
    date_intervention: str = Form(...),
    type: str = Form(...),
    parcelle_id: Optional[int] = Form(None),
    description: str = Form(..., min_length=1),
    duree_minutes: Optional[int] = Form(None),
):
    """Crée une intervention. Retourne la liste mise à jour."""
    execute(
        """INSERT INTO interventions (date_intervention, type, parcelle_id, description, duree_minutes)
           VALUES (?, ?, ?, ?, ?)""",
        (date_intervention, type, parcelle_id or None, description, duree_minutes),
    )
    # Rediriger vers la liste (HTMX suivra le redirect et mettra à jour le conteneur)
    return RedirectResponse(url="/journal/liste/interventions?page=1", status_code=303)


@router.delete("/interventions/{intervention_id}", response_class=HTMLResponse)
def supprimer_intervention(request: Request, intervention_id: int, page: int = 1):
    """Supprime une intervention. Retourne la liste mise à jour."""
    execute("DELETE FROM interventions WHERE id = ?", (intervention_id,))
    return RedirectResponse(
        url=f"/journal/liste/interventions?page={page}", status_code=303
    )


# ═══════════════════════════════════════════════════════════════
# CRUD — Observations
# ═══════════════════════════════════════════════════════════════

@router.post("/observations", response_class=HTMLResponse)
def creer_observation(
    request: Request,
    date_observation: str = Form(...),
    type: str = Form("observation"),
    parcelle_id: Optional[int] = Form(None),
    description: str = Form(..., min_length=1),
):
    """Crée une observation. Retourne la liste mise à jour."""
    execute(
        """INSERT INTO observations (date_observation, type, parcelle_id, description)
           VALUES (?, ?, ?, ?)""",
        (date_observation, type, parcelle_id or None, description),
    )
    return RedirectResponse(url="/journal/liste/observations?page=1", status_code=303)


@router.delete("/observations/{observation_id}", response_class=HTMLResponse)
def supprimer_observation(request: Request, observation_id: int, page: int = 1):
    """Supprime une observation. Retourne la liste mise à jour."""
    execute("DELETE FROM observations WHERE id = ?", (observation_id,))
    return RedirectResponse(
        url=f"/journal/liste/observations?page={page}", status_code=303
    )


# ═══════════════════════════════════════════════════════════════
# CRUD — Parcelles
# ═══════════════════════════════════════════════════════════════

@router.post("/parcelles", response_class=HTMLResponse)
def creer_parcelle(
    request: Request,
    nom: str = Form(..., min_length=1, max_length=100),
    surface_m2: Optional[float] = Form(None),
    exposition: Optional[str] = Form(None),
    type_sol: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
):
    """Crée une parcelle. Retourne la liste mise à jour."""
    execute(
        """INSERT INTO parcelles (nom, surface_m2, exposition, type_sol, notes)
           VALUES (?, ?, ?, ?, ?)""",
        (nom, surface_m2, exposition, type_sol, notes),
    )
    return RedirectResponse(url="/journal/liste/parcelles", status_code=303)


@router.delete("/parcelles/{parcelle_id}", response_class=HTMLResponse)
def supprimer_parcelle(request: Request, parcelle_id: int):
    """Supprime une parcelle. Retourne la liste mise à jour."""
    execute("DELETE FROM parcelles WHERE id = ?", (parcelle_id,))
    return RedirectResponse(url="/journal/liste/parcelles", status_code=303)
