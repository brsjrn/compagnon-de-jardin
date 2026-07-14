"""Modèles Pydantic pour le module 02 — Base de connaissances."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# --- Variétés (catalogue personnel) ---

class VarieteCreate(BaseModel):
    """Ajout d'une variété au catalogue personnel."""
    nom: str = Field(..., min_length=1, max_length=200)
    nom_latin: Optional[str] = None
    type: Optional[str] = None  # légume, fruit, aromatique, fleur, engrais_vert
    famille: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = "personnel"  # wikipedia, personnel, autre
    wiki_title: Optional[str] = None  # lien vers l'article Wikipedia


class VarieteResponse(BaseModel):
    """Représentation d'une variété du catalogue."""
    id: int
    nom: str
    nom_latin: Optional[str] = None
    type: Optional[str] = None
    famille: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None
    wiki_title: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Résultats de recherche ---

class SearchResult(BaseModel):
    """Résultat d'une recherche (Wikipedia ou catalogue local)."""
    title: str
    snippet: str = ""
    pageid: int = 0
    wordcount: int = 0
    source: str = "wikipedia"  # wikipedia | local
    variete_id: Optional[int] = None  # si déjà dans le catalogue local


# --- Types de légumes pour les filtres ---

TYPES_LEGUMES: list[str] = [
    "légume_fruit",     # tomate, courge, aubergine, poivron...
    "légume_racine",    # carotte, betterave, radis...
    "légume_feuille",   # salade, épinard, chou...
    "légume_tige",      # poireau, asperge, céleri...
    "légume_bulbe",     # oignon, ail, échalote...
    "légume_fleur",     # chou-fleur, brocoli, artichaut...
    "légume_gousse",    # haricot, pois, fève...
    "fruit",
    "aromatique",
    "fleur",
    "engrais_vert",
    "autre",
]

FAMILLES: list[str] = [
    "solanacées",
    "cucurbitacées",
    "fabacées",
    "brassicacées",
    "apiacées",
    "alliacées",
    "astéracées",
    "chénopodiacées",
    "lamiacées",
    "rosacées",
    "poacées",
    "autre",
]
