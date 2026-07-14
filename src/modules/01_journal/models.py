"""Modèles Pydantic pour le module Journal.

Validation des données entrantes (formulaires) et formatage
des réponses pour les templates.
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


# --- Parcelles ---

class ParcelleCreate(BaseModel):
    """Création d'une parcelle."""
    nom: str = Field(..., min_length=1, max_length=100)
    surface_m2: Optional[float] = None
    exposition: Optional[str] = None
    type_sol: Optional[str] = None
    notes: Optional[str] = None


class ParcelleResponse(BaseModel):
    """Représentation d'une parcelle existante."""
    id: int
    nom: str
    surface_m2: Optional[float] = None
    exposition: Optional[str] = None
    type_sol: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Interventions ---

class InterventionCreate(BaseModel):
    """Création d'une intervention."""
    date_intervention: date = Field(default_factory=date.today)
    type: str = Field(..., min_length=1, max_length=50)
    parcelle_id: Optional[int] = None
    description: str = Field(..., min_length=1)
    duree_minutes: Optional[int] = Field(None, ge=0)
    # Photo upload sera géré séparément (futur)


class InterventionResponse(BaseModel):
    """Représentation d'une intervention existante."""
    id: int
    date_intervention: date
    type: str
    parcelle_id: Optional[int] = None
    parcelle_nom: Optional[str] = None  # jointure
    description: str
    duree_minutes: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Observations ---

class ObservationCreate(BaseModel):
    """Création d'une observation."""
    date_observation: date = Field(default_factory=date.today)
    type: str = Field(default="observation")
    parcelle_id: Optional[int] = None
    description: str = Field(..., min_length=1)


class ObservationResponse(BaseModel):
    """Représentation d'une observation existante."""
    id: int
    date_observation: date
    type: str
    parcelle_id: Optional[int] = None
    parcelle_nom: Optional[str] = None
    description: str
    chemin_fichier: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Types disponibles pour les listes déroulantes ---

TYPES_INTERVENTION: list[str] = [
    "préparation_sol",
    "semis",
    "plantation",
    "arrosage",
    "désherbage",
    "paillage",
    "taille",
    "traitement",
    "amendement",
    "récolte",
    "autre",
]

TYPES_OBSERVATION: list[str] = [
    "observation",
    "météo",
    "incident",
    "photo",
    "note_vocale",
    "autre",
]
