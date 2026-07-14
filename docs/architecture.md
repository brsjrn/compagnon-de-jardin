# Architecture logicielle

> Vue détaillée de l'architecture du Compagnon de jardin.
> Ce document est évolutif : il s'enrichit au fur et à mesure du développement.

---

## Principes architecturaux

1. **Modularité** : chaque module (`01-journal`, `02-connaissances`, etc.) est un package Python indépendant. Il expose un routeur FastAPI et peut fonctionner sans les autres modules.

2. **Pas d'ORM** : on utilise SQLite directement (`sqlite3` stdlib) avec des helpers légers. Le schéma est versionné dans `src/db/schema.sql`. Les migrations se font via des scripts SQL incrémentaux (futur dossier `src/db/migrations/`).

3. **SSR + HTMX** : le rendu se fait côté serveur (Jinja2). HTMX gère l'interactivité (requêtes AJAX, mise à jour partielle du DOM) sans JavaScript custom.

4. **API interne** : chaque module expose ses endpoints FastAPI. Les modules communiquent entre eux via des appels de fonctions Python (imports explicites), pas via HTTP.

5. **Stateless** : le serveur ne stocke pas d'état en mémoire. Tout est persisté dans SQLite.

---

## Flux de données

```
[Smartphone au jardin]
    │
    ├── Saisie texte / photo / note vocale
    │   → POST /journal/interventions
    │   → POST /journal/observations
    │
    ├── Consultation
    │   → GET /journal
    │   → GET /planification/calendrier
    │
    └── Assistant
        → POST /assistant/ask  (→ API Deepseek + RAG DB locale)

[PC de bureau]
    │
    ├── Planification, analyse, exports
    └── Administration
```

---

## Base de données

Voir `src/db/schema.sql` pour le DDL complet.

### Tables principales (Module 01 — Journal)

| Table | Rôle |
|---|---|
| `parcelles` | Les zones du jardin, avec leurs caractéristiques |
| `varietes` | Fiches personnelles de variétés cultivées |
| `cultures` | Une occurrence de culture (variété + parcelle + période) |
| `interventions` | Actions réalisées (semis, arrosage, récolte...) |
| `recoltes` | Récoltes détaillées (quantité, qualité) |
| `observations` | Notes libres, photos, incidents |

### Tables futures (Modules 03-04)

| Table | Rôle |
|---|---|
| `planifications` | Calendrier prévisionnel (Module 03) |
| `rotations` | Règles et historique de rotation (Module 03) |
| `meteo` | Données météo externes, déjà prévue dans le schéma |
| `capteurs_data` | Données de capteurs locaux, déjà prévue dans le schéma |

---

## Module 01 — Journal

**Fichiers :** `src/modules/01-journal/`

Le journal est le module fondateur. Il permet :
- CRUD sur les tables `interventions`, `observations`, `recoltes`
- Saisie rapide (interface mobile-first)
- Consultation par date, parcelle, type
- Association de photos et notes vocales

**Endpoints prévus :**
- `GET /journal` — tableau de bord du journal
- `POST /journal/interventions` — nouvelle intervention
- `GET /journal/interventions?date=&parcelle_id=` — liste filtrée
- `POST /journal/observations` — nouvelle observation
- `POST /journal/recoltes` — nouvelle récolte

---

## Déploiement

En phase de développement :
```bash
make dev    # uvicorn --reload sur localhost:8000
```

En phase d'usage (sur PC fixe au domicile) :
```bash
make run    # uvicorn sans reload
```

Le smartphone accède au serveur via le réseau local (WiFi). En cas d'absence de réseau, la PWA permet une utilisation dégradée (consultation du cache, saisie différée ?).

---

*Dernière mise à jour : 2026-07-14*
