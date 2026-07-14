"""Gestion de la connexion à la base de données SQLite.

Pas d'ORM : on utilise sqlite3 de la stdlib, avec un Row factory
pour avoir des résultats indexables par nom de colonne.
"""

import sqlite3
from pathlib import Path

from src.config import DB_PATH, SCHEMA_PATH, PROJECT_ROOT


def get_connection() -> sqlite3.Connection:
    """Retourne une connexion SQLite avec Row factory."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")  # Meilleure concurrence
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    """Initialise la base de données en exécutant le schéma SQL."""
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    conn = get_connection()
    try:
        conn.executescript(schema)
        conn.commit()
        print(f"✓ Base initialisée : {DB_PATH}")
    finally:
        conn.close()


def query(sql: str, params: tuple | dict | None = None) -> list[sqlite3.Row]:
    """Exécute une requête SELECT et retourne les résultats."""
    conn = get_connection()
    try:
        cursor = conn.execute(sql, params or ())
        return cursor.fetchall()
    finally:
        conn.close()


def execute(sql: str, params: tuple | dict | None = None) -> int:
    """Exécute une requête INSERT/UPDATE/DELETE et retourne le lastrowid."""
    conn = get_connection()
    try:
        cursor = conn.execute(sql, params or ())
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def execute_many(sql: str, params_list: list[tuple | dict]) -> None:
    """Exécute une requête avec plusieurs jeux de paramètres."""
    conn = get_connection()
    try:
        conn.executemany(sql, params_list)
        conn.commit()
    finally:
        conn.close()
