"""Fixtures partagées pour les tests."""

import tempfile
from pathlib import Path

import pytest

# Forcer l'utilisation d'une base temporaire avant tout import des modules src
# (car src.config est évalué au moment de l'import)
@pytest.fixture(autouse=True)
def temp_db(monkeypatch, tmp_path: Path):
    """Redirige la DB vers un fichier temporaire le temps du test."""
    db_path = tmp_path / "test_compagnon.db"
    schema_path = (
        Path(__file__).resolve().parent.parent / "src" / "db" / "schema.sql"
    )

    monkeypatch.setattr("src.config.DB_PATH", db_path)
    monkeypatch.setattr("src.config.SCHEMA_PATH", schema_path)

    # Créer le schéma
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    conn.executescript(schema_path.read_text(encoding="utf-8"))
    conn.commit()
    conn.close()

    yield db_path


@pytest.fixture
def client():
    """Client de test FastAPI."""
    from src.main import app
    from fastapi.testclient import TestClient

    return TestClient(app)
