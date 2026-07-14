"""Client Wikipedia pour la base de connaissances.

Utilise l'API REST de Wikipedia (gratuite, pas de clé requise)
avec cache local dans SQLite pour le mode hors-ligne et la frugalité réseau.
"""

import json
import time
from typing import Optional

import httpx

from src.db.connection import execute, query

# Langue par défaut
DEFAULT_LANG = "fr"

# URLs de l'API
API_REST = "https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}"
API_SEARCH = (
    "https://{lang}.wikipedia.org/w/api.php"
    "?action=query&list=search&srsearch={query}&format=json&srlimit=10"
)

# User-Agent conforme aux recommandations Wikipedia
USER_AGENT = "CompagnonDeJardin/0.1 (https://github.com/brsjrn/compagnon-de-jardin)"


def _cache_key(title: str, lang: str = DEFAULT_LANG) -> str:
    """Normalise le titre pour le cache."""
    return title.strip().replace(" ", "_").capitalize()


def _get_from_cache(title: str, lang: str = DEFAULT_LANG) -> Optional[dict]:
    """Récupère une entrée du cache local si elle existe."""
    key = _cache_key(title, lang)
    rows = query(
        "SELECT * FROM wiki_cache WHERE title = ? AND lang = ?",
        (key, lang),
    )
    if rows:
        return dict(rows[0])
    return None


def _save_to_cache(title: str, lang: str, data: dict) -> None:
    """Enregistre un résultat Wikipedia dans le cache local."""
    key = _cache_key(title, lang)
    execute(
        """INSERT OR REPLACE INTO wiki_cache
           (title, lang, extract, extract_html, thumbnail_url, page_url, raw_json)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            key,
            lang,
            data.get("extract", ""),
            data.get("extract_html", ""),
            data.get("thumbnail", {}).get("source", ""),
            data.get("content_urls", {}).get("desktop", {}).get("page", ""),
            json.dumps(data, ensure_ascii=False),
        ),
    )


async def search_wikipedia(query_str: str, lang: str = DEFAULT_LANG) -> list[dict]:
    """Recherche des articles Wikipedia correspondant à une requête.

    Returns:
        Liste de dicts avec 'title', 'pageid', 'snippet'
    """
    url = API_SEARCH.format(lang=lang, query=query_str)
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, headers={"User-Agent": USER_AGENT})
        resp.raise_for_status()
        data = resp.json()

    results = []
    for hit in data.get("query", {}).get("search", []):
        results.append(
            {
                "title": hit["title"],
                "pageid": hit["pageid"],
                "snippet": _clean_html(hit.get("snippet", "")),
                "wordcount": hit.get("wordcount", 0),
            }
        )
    return results


async def get_article_summary(
    title: str, lang: str = DEFAULT_LANG, use_cache: bool = True
) -> dict:
    """Récupère le résumé d'un article Wikipedia (avec cache local).

    Returns:
        Dict avec 'title', 'extract', 'extract_html', 'thumbnail_url',
        'page_url', 'lang', 'from_cache'
    """
    key = _cache_key(title, lang)

    # Vérifier le cache
    if use_cache:
        cached = _get_from_cache(title, lang)
        if cached:
            return {
                "title": cached["title"],
                "extract": cached["extract"],
                "extract_html": cached["extract_html"],
                "thumbnail_url": cached["thumbnail_url"],
                "page_url": cached["page_url"],
                "lang": cached["lang"],
                "from_cache": True,
            }

    # Appel API
    url = API_REST.format(lang=lang, title=key)
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            url,
            headers={"User-Agent": USER_AGENT},
            follow_redirects=True,
        )
        if resp.status_code == 404:
            return {
                "title": title,
                "extract": "Aucun article trouvé sur Wikipedia.",
                "extract_html": "",
                "thumbnail_url": "",
                "page_url": "",
                "lang": lang,
                "from_cache": False,
                "error": "not_found",
            }
        resp.raise_for_status()
        data = resp.json()

    # Mettre en cache
    _save_to_cache(title, lang, data)

    return {
        "title": data.get("title", title),
        "extract": data.get("extract", ""),
        "extract_html": data.get("extract_html", ""),
        "thumbnail_url": data.get("thumbnail", {}).get("source", ""),
        "page_url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
        "lang": lang,
        "from_cache": False,
    }


def _clean_html(html: str) -> str:
    """Supprime les balises HTML basiques d'un snippet Wikipedia."""
    import re

    text = re.sub(r"<[^>]+>", "", html)
    text = text.replace("&amp;", "&").replace("&quot;", '"').replace("&lt;", "<")
    text = text.replace("&gt;", ">").replace("&#039;", "'").replace("&nbsp;", " ")
    return text.strip()
