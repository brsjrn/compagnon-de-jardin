"""Modèles pour le module 03 — Planification."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class CulturePlanCreate(BaseModel):
    """Création d'une culture planifiée."""
    parcelle_id: int
    variete_id: int
    date_semis: Optional[date] = None
    date_plantation: Optional[date] = None
    date_premiere_recolte: Optional[date] = None
    date_arrachage: Optional[date] = None
    quantite_plantee: Optional[int] = None
    statut: str = "planifié"
    notes: Optional[str] = None


STATUTS: list[str] = ["planifié", "en_cours", "terminé"]

MOIS: list[str] = [
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre",
]

# Couleurs par famille pour le calendrier
COULEURS_FAMILLE: dict[str, str] = {
    "solanacées": "#e8daef",
    "cucurbitacées": "#d5f5e3",
    "fabacées": "#d4edda",
    "brassicacées": "#cfe2ff",
    "apiacées": "#f5e6d3",
    "alliacées": "#fff3cd",
    "astéracées": "#fadbd8",
    "chénopodiacées": "#d5dbdb",
    "lamiacées": "#e8daef",
    "rosacées": "#f5b7b1",
    "poacées": "#abebc6",
}
COULEUR_DEFAUT = "#eaecee"
