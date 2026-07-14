"""Routes du module 03 — Planification.

Calendrier de cultures, planification par parcelles, rotations.
"""

import importlib as _importlib
from datetime import date
from typing import Optional

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.db.connection import execute, query
from src.templating import templates

_mod = _importlib.import_module("src.modules.03_planification.models")
MOIS = _mod.MOIS
COULEURS_FAMILLE = _mod.COULEURS_FAMILLE
COULEUR_DEFAUT = _mod.COULEUR_DEFAUT
STATUTS = _mod.STATUTS

router = APIRouter(prefix="/planification", tags=["Planification"])


# ═══════════════════════════════════════════════════════════════
# Page principale
# ═══════════════════════════════════════════════════════════════

@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
def planification_index(request: Request):
    """Page principale de planification."""
    annee = date.today().year
    nb_planifie = query(
        "SELECT COUNT(*) as n FROM cultures WHERE statut = 'planifié'"
    )[0]["n"]
    nb_en_cours = query(
        "SELECT COUNT(*) as n FROM cultures WHERE statut = 'en_cours'"
    )[0]["n"]
    nb_parcelles = query("SELECT COUNT(*) as n FROM parcelles")[0]["n"]

    return templates.TemplateResponse(
        request=request,
        name="planification/index.html",
        context={
            "annee": annee,
            "nb_planifie": nb_planifie,
            "nb_en_cours": nb_en_cours,
            "nb_parcelles": nb_parcelles,
        },
    )


# ═══════════════════════════════════════════════════════════════
# Calendrier (vue Gantt simplifiée)
# ═══════════════════════════════════════════════════════════════

@router.get("/calendrier", response_class=HTMLResponse)
def calendrier(request: Request, annee: Optional[int] = None):
    """Vue calendrier : planning annuel par mois et parcelles."""
    if annee is None:
        annee = date.today().year

    # Récupérer toutes les cultures (planifiées + en cours) pour l'année
    rows = query(
        """SELECT c.*, v.nom AS variete_nom, v.famille, v.type,
                  p.nom AS parcelle_nom
           FROM cultures c
           JOIN varietes v ON c.variete_id = v.id
           JOIN parcelles p ON c.parcelle_id = p.id
           WHERE c.statut IN ('planifié', 'en_cours')
             AND (
                 (c.date_semis >= ? AND c.date_semis < ?)
                 OR (c.date_plantation >= ? AND c.date_plantation < ?)
                 OR (c.date_premiere_recolte >= ? AND c.date_premiere_recolte < ?)
                 OR (c.date_semis < ? AND (c.date_arrachage IS NULL OR c.date_arrachage >= ?))
             )
           ORDER BY p.nom, c.date_semis""",
        (
            f"{annee}-01-01", f"{annee + 1}-01-01",
            f"{annee}-01-01", f"{annee + 1}-01-01",
            f"{annee}-01-01", f"{annee + 1}-01-01",
            f"{annee + 1}-01-01", f"{annee}-01-01",
        ),
    )

    cultures = [dict(r) for r in rows]

    # Pondération par mois pour le calendrier : calculer quels mois sont couverts
    cultures_avec_mois = []
    for c in cultures:
        mois_actifs = _mois_actifs(c, annee)
        cultures_avec_mois.append({**c, "mois_actifs": mois_actifs})

    parcelles = query("SELECT id, nom FROM parcelles ORDER BY nom")
    varietes = query("SELECT id, nom FROM varietes ORDER BY nom")

    return templates.TemplateResponse(
        request=request,
        name="planification/partials/calendrier.html",
        context={
            "annee": annee,
            "annee_prec": annee - 1,
            "annee_suiv": annee + 1,
            "mois": MOIS,
            "cultures": cultures_avec_mois,
            "parcelles": [dict(p) for p in parcelles],
            "varietes": [dict(v) for v in varietes],
            "couleurs_famille": COULEURS_FAMILLE,
            "couleur_defaut": COULEUR_DEFAUT,
        },
    )


def _mois_actifs(culture: dict, annee: int) -> list[int]:
    """Détermine quels mois (1-12) une culture est active."""
    debut = None
    fin = None

    for champ in ["date_semis", "date_plantation"]:
        if culture.get(champ):
            d = date.fromisoformat(culture[champ])
            if debut is None or d < debut:
                debut = d

    if culture.get("date_arrachage"):
        fin = date.fromisoformat(culture["date_arrachage"])
    elif culture.get("date_premiere_recolte"):
        fin = date.fromisoformat(culture["date_premiere_recolte"])

    if debut is None:
        return []

    if fin is None:
        # Estimer : +3 mois après le début
        fin = debut.replace(month=((debut.month + 3) % 12) or 12)
        if fin < debut:
            fin = fin.replace(year=debut.year + 1)

    actifs = []
    current = debut
    while current <= fin:
        if current.year == annee:
            actifs.append(current.month)
        # Avancer d'un mois
        m = current.month + 1
        y = current.year
        if m > 12:
            m = 1
            y += 1
        current = current.replace(year=y, month=m, day=1)
        if current.year > annee + 1:
            break

    return actifs


# ═══════════════════════════════════════════════════════════════
# Vue par parcelles
# ═══════════════════════════════════════════════════════════════

@router.get("/parcelles", response_class=HTMLResponse)
def vue_parcelles(request: Request):
    """Vue planning par parcelle : ce qui est prévu où."""
    parcelles = query("SELECT * FROM parcelles ORDER BY nom")
    cultures = query(
        """SELECT c.*, v.nom AS variete_nom, v.famille, v.type
           FROM cultures c
           JOIN varietes v ON c.variete_id = v.id
           WHERE c.statut IN ('planifié', 'en_cours')
           ORDER BY c.date_semis"""
    )

    # Grouper par parcelle
    cultures_par_parcelle: dict[int, list] = {}
    for c in cultures:
        c_dict = dict(c)
        pid = c_dict["parcelle_id"]
        if pid not in cultures_par_parcelle:
            cultures_par_parcelle[pid] = []
        cultures_par_parcelle[pid].append(c_dict)

    return templates.TemplateResponse(
        request=request,
        name="planification/partials/parcelles_plan.html",
        context={
            "parcelles": [dict(p) for p in parcelles],
            "cultures_par_parcelle": cultures_par_parcelle,
        },
    )


# ═══════════════════════════════════════════════════════════════
# Rotations
# ═══════════════════════════════════════════════════════════════

@router.get("/rotations", response_class=HTMLResponse)
def rotations(request: Request):
    """Historique des cultures par parcelle pour suggérer les rotations."""
    parcelles = query("SELECT * FROM parcelles ORDER BY nom")
    cultures = query(
        """SELECT c.*, v.nom AS variete_nom, v.famille, v.type,
                  p.nom AS parcelle_nom
           FROM cultures c
           JOIN varietes v ON c.variete_id = v.id
           JOIN parcelles p ON c.parcelle_id = p.id
           ORDER BY p.nom, c.date_semis DESC"""
    )

    return templates.TemplateResponse(
        request=request,
        name="planification/partials/rotations.html",
        context={
            "parcelles": [dict(p) for p in parcelles],
            "cultures": [dict(c) for c in cultures],
            "couleurs_famille": COULEURS_FAMILLE,
            "couleur_defaut": COULEUR_DEFAUT,
        },
    )


# ═══════════════════════════════════════════════════════════════
# CRUD — Culture planifiée
# ═══════════════════════════════════════════════════════════════

@router.get("/form", response_class=HTMLResponse)
def form_culture(request: Request, parcelle_id: int = 0, variete_id: int = 0):
    """Formulaire pour planifier une nouvelle culture."""
    parcelles = query("SELECT id, nom FROM parcelles ORDER BY nom")
    varietes = query("SELECT id, nom, famille FROM varietes ORDER BY nom")

    return templates.TemplateResponse(
        request=request,
        name="planification/partials/culture_form.html",
        context={
            "today": date.today().isoformat(),
            "parcelles": [dict(p) for p in parcelles],
            "varietes": [dict(v) for v in varietes],
            "statuts": STATUTS,
            "preselected_parcelle": parcelle_id,
            "preselected_variete": variete_id,
        },
    )


@router.post("/cultures", response_class=HTMLResponse)
def creer_culture(
    request: Request,
    parcelle_id: int = Form(...),
    variete_id: int = Form(...),
    date_semis: Optional[str] = Form(None),
    date_plantation: Optional[str] = Form(None),
    date_premiere_recolte: Optional[str] = Form(None),
    date_arrachage: Optional[str] = Form(None),
    quantite_plantee: Optional[int] = Form(None),
    statut: str = Form("planifié"),
    notes: Optional[str] = Form(None),
):
    """Crée une culture planifiée."""
    execute(
        """INSERT INTO cultures
           (parcelle_id, variete_id, date_semis, date_plantation,
            date_premiere_recolte, date_arrachage, quantite_plantee, statut, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            parcelle_id, variete_id,
            date_semis or None, date_plantation or None,
            date_premiere_recolte or None, date_arrachage or None,
            quantite_plantee, statut, notes,
        ),
    )
    return RedirectResponse(url="/planification/calendrier", status_code=303)


@router.put("/cultures/{culture_id}/statut", response_class=HTMLResponse)
def changer_statut(request: Request, culture_id: int, statut: str = Form(...)):
    """Change le statut d'une culture."""
    execute("UPDATE cultures SET statut = ? WHERE id = ?", (statut, culture_id))
    return RedirectResponse(url="/planification/calendrier", status_code=303)


@router.delete("/cultures/{culture_id}", response_class=HTMLResponse)
def supprimer_culture(request: Request, culture_id: int):
    """Supprime une culture planifiée."""
    execute("DELETE FROM cultures WHERE id = ?", (culture_id,))
    return RedirectResponse(url="/planification/calendrier", status_code=303)
