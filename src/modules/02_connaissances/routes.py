"""Routes du module 02 — Base de connaissances.

Recherche Wikipedia + catalogue personnel de variétés.
"""

import importlib as _importlib
from typing import Optional

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.db.connection import execute, query
from src.templating import templates

_wiki = _importlib.import_module("src.modules.02_connaissances.wikipedia")
_mod = _importlib.import_module("src.modules.02_connaissances.models")
get_article_summary = _wiki.get_article_summary
search_wikipedia = _wiki.search_wikipedia
FAMILLES = _mod.FAMILLES
TYPES_LEGUMES = _mod.TYPES_LEGUMES

router = APIRouter(prefix="/connaissances", tags=["Connaissances"])


# ═══════════════════════════════════════════════════════════════
# Page principale
# ═══════════════════════════════════════════════════════════════

@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
def connaissances_index(request: Request):
    """Page principale avec recherche Wikipedia + catalogue."""
    # Statistiques rapides
    nb_varietes = query("SELECT COUNT(*) as n FROM varietes")[0]["n"]
    nb_parcelles = query("SELECT COUNT(*) as n FROM parcelles")[0]["n"]
    nb_wiki_cache = query("SELECT COUNT(*) as n FROM wiki_cache")[0]["n"]

    return templates.TemplateResponse(
        request=request,
        name="connaissances/index.html",
        context={
            "nb_varietes": nb_varietes,
            "nb_parcelles": nb_parcelles,
            "nb_wiki_cache": nb_wiki_cache,
        },
    )


# ═══════════════════════════════════════════════════════════════
# Recherche Wikipedia
# ═══════════════════════════════════════════════════════════════

@router.get("/recherche", response_class=HTMLResponse)
async def rechercher(request: Request, q: str = ""):
    """Recherche Wikipedia et affiche les résultats."""
    if not q or len(q.strip()) < 2:
        return templates.TemplateResponse(
            request=request,
            name="connaissances/partials/search_results.html",
            context={"results": [], "query": q, "error": "Entrez au moins 2 caractères."},
        )

    try:
        raw_results = await search_wikipedia(q.strip())
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="connaissances/partials/search_results.html",
            context={"results": [], "query": q, "error": f"Erreur Wikipedia : {e}"},
        )

    # Vérifier si chaque résultat est déjà dans le catalogue local
    existing = {
        r["nom"]: r["id"]
        for r in query("SELECT id, nom FROM varietes")
    }

    results = []
    for r in raw_results:
        results.append({
            "title": r["title"],
            "snippet": r["snippet"],
            "pageid": r["pageid"],
            "wordcount": r["wordcount"],
            "source": "wikipedia",
            "in_catalog": r["title"] in existing,
            "variete_id": existing.get(r["title"]),
        })

    # Chercher aussi dans le catalogue local
    if q:
        local_rows = query(
            "SELECT id, nom, type, famille FROM varietes WHERE nom LIKE ? LIMIT 5",
            (f"%{q}%",),
        )
        for r in local_rows:
            if not any(res["title"] == r["nom"] for res in results):
                results.insert(0, {
                    "title": r["nom"],
                    "snippet": f"{r['type'] or ''} — {r['famille'] or ''}".strip(" —"),
                    "pageid": 0,
                    "wordcount": 0,
                    "source": "local",
                    "in_catalog": True,
                    "variete_id": r["id"],
                })

    return templates.TemplateResponse(
        request=request,
        name="connaissances/partials/search_results.html",
        context={"results": results, "query": q, "error": None},
    )


# ═══════════════════════════════════════════════════════════════
# Consultation Wikipedia
# ═══════════════════════════════════════════════════════════════

@router.get("/wiki/{title:path}", response_class=HTMLResponse)
async def consulter_wikipedia(request: Request, title: str):
    """Affiche le résumé Wikipedia d'un article (avec cache)."""
    try:
        article = await get_article_summary(title)
    except Exception as e:
        return HTMLResponse(f"<p>Erreur : {e}</p>", status_code=502)

    # Vérifier si déjà dans le catalogue
    existing = query("SELECT id FROM varietes WHERE nom = ?", (title,))
    variete_id = existing[0]["id"] if existing else None

    return templates.TemplateResponse(
        request=request,
        name="connaissances/partials/wiki_detail.html",
        context={
            "article": article,
            "variete_id": variete_id,
            "types": TYPES_LEGUMES,
            "familles": FAMILLES,
        },
    )


# ═══════════════════════════════════════════════════════════════
# Catalogue personnel — Variétés
# ═══════════════════════════════════════════════════════════════

@router.get("/varietes", response_class=HTMLResponse)
def mes_varietes(
    request: Request,
    type_filter: Optional[str] = None,
):
    """Liste les variétés du catalogue personnel."""
    conditions = []
    params: list = []
    if type_filter:
        conditions.append("type = ?")
        params.append(type_filter)
    where = " AND ".join(conditions) if conditions else "1=1"

    rows = query(
        f"SELECT * FROM varietes WHERE {where} ORDER BY nom",
        params,
    )

    return templates.TemplateResponse(
        request=request,
        name="connaissances/partials/varietes_list.html",
        context={
            "varietes": [dict(r) for r in rows],
            "types": TYPES_LEGUMES,
            "familles": FAMILLES,
            "type_filter": type_filter or "",
        },
    )


@router.get("/varietes/{variete_id}", response_class=HTMLResponse)
def detail_variete(request: Request, variete_id: int):
    """Détail d'une variété du catalogue."""
    rows = query("SELECT * FROM varietes WHERE id = ?", (variete_id,))
    if not rows:
        return HTMLResponse("<p>Variété introuvable.</p>", status_code=404)

    variete = dict(rows[0])

    # Cultures associées (depuis le journal)
    cultures = query(
        """SELECT c.*, p.nom as parcelle_nom
           FROM cultures c
           LEFT JOIN parcelles p ON c.parcelle_id = p.id
           WHERE c.variete_id = ?
           ORDER BY c.date_semis DESC""",
        (variete_id,),
    )

    return templates.TemplateResponse(
        request=request,
        name="connaissances/partials/variete_detail.html",
        context={
            "variete": variete,
            "cultures": [dict(c) for c in cultures],
            "types": TYPES_LEGUMES,
            "familles": FAMILLES,
        },
    )


@router.post("/varietes", response_class=HTMLResponse)
def ajouter_variete(
    request: Request,
    nom: str = Form(..., min_length=1, max_length=200),
    nom_latin: Optional[str] = Form(None),
    type: Optional[str] = Form(None),
    famille: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    source: Optional[str] = Form("personnel"),
    wiki_title: Optional[str] = Form(None),
):
    """Ajoute une variété au catalogue personnel."""
    execute(
        """INSERT INTO varietes (nom, nom_latin, type, famille, description, source, wiki_title)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (nom, nom_latin, type, famille, description, source, wiki_title),
    )
    return RedirectResponse(url="/connaissances/varietes", status_code=303)


@router.delete("/varietes/{variete_id}", response_class=HTMLResponse)
def supprimer_variete(request: Request, variete_id: int):
    """Supprime une variété du catalogue."""
    execute("DELETE FROM varietes WHERE id = ?", (variete_id,))
    return RedirectResponse(url="/connaissances/varietes", status_code=303)


# ═══════════════════════════════════════════════════════════════
# HTMX — Formulaires
# ═══════════════════════════════════════════════════════════════

@router.get("/form/variete", response_class=HTMLResponse)
def form_variete(
    request: Request,
    nom: str = "",
    nom_latin: str = "",
    type_: str = "",
    famille: str = "",
    wiki_title: str = "",
    description: str = "",
):
    """Formulaire d'ajout manuel d'une variété."""
    return templates.TemplateResponse(
        request=request,
        name="connaissances/partials/variete_form.html",
        context={
            "types": TYPES_LEGUMES,
            "familles": FAMILLES,
            "prefill_nom": nom,
            "prefill_nom_latin": nom_latin,
            "prefill_type": type_,
            "prefill_famille": famille,
            "prefill_wiki_title": wiki_title,
            "prefill_description": description,
        },
    )
