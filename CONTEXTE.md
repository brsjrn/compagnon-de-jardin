# CONTEXTE.md — Tableau de bord du projet

> **Point d'entrée unique pour tout LLM (ou humain) reprenant le projet.**
> À lire en premier. Mis à jour à chaque session de travail.

---

## Identité du projet

**Compagnon de jardin** — Système hybride (pratiques de jardinage + outils numériques + IA) conçu pour accompagner la création et l'évolution d'un potager nourricier. Il ne s'agit pas d'automatiser le jardinage, mais d'assister les prises de décision sans se substituer au jugement humain. Voir `MANIFESTE.md` pour l'intention, `CAHIER_DES_CHARGES.md` pour le périmètre complet.

---

## État d'avancement

### Fait
- [x] Rédaction du manifeste (v1)
- [x] Rédaction du cahier des charges (v1, généré par ChatGPT)
- [x] Structuration du projet (arborescence, socle technique)
- [x] Initialisation Git + push GitHub
- [x] **Étape 0 — Socle technique** : environnement Python, FastAPI fonctionnel, schéma DB (9 tables), page d'accueil
- [x] **Module 01 — Journal de culture** : CRUD interventions, observations, parcelles. Interface HTMX à 3 onglets avec filtres et pagination. Testé et fonctionnel.
- [x] **Module 02 — Base de connaissances** : recherche Wikipedia, catalogue personnel de variétés, cache local des articles. Interface avec barre de recherche, détail article, ajout au catalogue. Testé et fonctionnel.
- [x] **Module 03 — Planification** : calendrier Gantt annuel, planification par parcelles, suivi des rotations, changement de statut (planifié→en_cours→terminé). Testé et fonctionnel.

### En cours
- [ ] **Module 04 — Capteurs** (prochaine étape)

### À faire (priorisé)
1. **Module 04 — Capteurs** : données météo (API open data Open-Meteo), puis capteurs locaux ← **PROCHAINE ACTION**
2. **Module 05 — Assistant IA** : interface conversationnelle (Deepseek) avec contexte du jardin

---

## Carte du projet

```
compagnon-de-jardin/
│
├── CONTEXTE.md              ← CE FICHIER. Tableau de bord. Lu en premier.
├── MANIFESTE.md             ← Intention fondatrice. Ne change quasiment jamais.
├── CAHIER_DES_CHARGES.md    ← Périmètre complet, modules, critères. Révisé annuellement.
├── QUESTIONS_OUVERTES.md    ← Points à trancher plus tard, hypothèses à vérifier.
├── README.md                ← Présentation pour humains.
│
├── pyproject.toml           ← Dépendances et métadonnées Python
├── Makefile                 ← Commandes usuelles : make run, make test, make db-init
├── .gitignore
│
├── src/
│   ├── main.py              ← Point d'entrée FastAPI
│   ├── config.py            ← Configuration centralisée (chemins, DB, API keys via .env)
│   ├── templating.py        ← Templates Jinja2 partagés (évite imports circulaires)
│   ├── db/
│   │   ├── schema.sql       ← Schéma SQLite (DDL)
│   │   └── connection.py    ← Connexion et helpers DB
│   ├── modules/
│   │   ├── 01_journal/      ← Module 01 — mémoire du jardin (FAIT ✓)
│   │   ├── 02_connaissances/← Module 02 — savoirs externes + personnels (FAIT ✓)
│   │   ├── 03_planification/← Module 03 — projections, calendrier (FAIT ✓)
│   │   ├── 04_capteurs/     ← Module 04 — données environnementales (à faire)
│   │   └── 05_assistant/    ← Module 05 — IA conversationnelle (à faire)
│   ├── templates/           ← Templates Jinja2 (HTML, HTMX)
│   └── static/              ← CSS, JS léger, manifest PWA
│
├── data/                    ← Base SQLite, exports (gitignoré sauf .gitkeep)
├── docs/
│   ├── architecture.md      ← Architecture logicielle détaillée
│   └── decisions.md         ← Registre des décisions architecturales (ADR)
└── tests/                   ← Tests unitaires et d'intégration
```

---

## Stack technique

| Brique | Choix | Version |
|---|---|---|
| Langage | Python | 3.11+ |
| Framework web | FastAPI | 0.115+ |
| Serveur ASGI | Uvicorn | 0.34+ |
| Base de données | SQLite | Intégré |
| Templates | Jinja2 | 3.1+ |
| Interactivité | HTMX (CDN) + vanilla JS | 2.0+ |
| IA | Deepseek API via lib openai | Compatible |
| Tests | Pytest | 8+ |
| PWA | Manifest JSON + Service Worker minimal | — |

---

## Conventions de code

- **Langue** : français pour la documentation, anglais pour le code (variables, fonctions, commentaires)
- **Nommage** : snake_case pour les fichiers Python, kebab-case pour les dossiers
- **Formatage** : Black (longueur de ligne 100), isort pour les imports
- **Types** : annotations de type obligatoires sur toutes les signatures de fonction
- **Docstrings** : format Google pour toutes les fonctions publiques
- **Modularité** : chaque module est indépendant. Pas d'imports circulaires entre modules.
- **Chemin DB** : `data/compagnon.db` (SQLite, un seul fichier)
- **Variables d'environnement** : fichier `.env` à la racine (non versionné). Template : `.env.example`

---

## Dépendances entre modules

```
01-journal ──► (aucune)        ← module fondateur, autonome
02-connaissances ─► (aucune)   ← autonome, mais ses données viennent de l'extérieur
03-planification ─► 01-journal + 02-connaissances
04-capteurs ─► 01-journal      ← les données de capteurs alimentent le journal
05-assistant ─► tous les autres modules (lecture seule)
```

Le graphe est un DAG. Aucun cycle. Chaque module peut être développé, testé et déployé indépendamment.

---

## Décisions clés

1. **SQLite et pas PostgreSQL** : cohérent avec la valeur de frugalité. Un fichier, zéro serveur, sauvegarde triviale. Amplement suffisant pour l'échelle d'un potager familial.
2. **FastAPI et pas Django** : plus léger, auto-documenté (OpenAPI), async natif, meilleur pour une API + SSR léger.
3. **HTMX et pas React/Vue** : la complexité d'un framework SPA n'est pas justifiée. Tes compétences HTML/CSS suffisent. HTMX ajoute l'interactivité sans couche JS lourde.
4. **Module 01 en premier** : la mémoire du jardin est le socle. Sans historique, les autres modules n'ont rien à analyser.
5. **Pas d'ORM (on utilise SQL direct)** : la base est simple, un ORM ajouterait une couche d'abstraction inutile et opaque. On utilise `sqlite3` de la stdlib avec des helpers légers.
6. **Deepseek plutôt qu'OpenAI** : coût, qualité équivalente, et tu l'utilises déjà.

---

## Prochaine action

> **Module 04 — Capteurs** : intégration API météo Open-Meteo (gratuite, sans clé), visualisation des données, et préparation pour capteurs locaux (ESP32).

---

## Notes techniques pour le vibe-coding

### Lancement du projet
```bash
cd ~/Programmation/sources/compagnon-de-jardin
source .venv/bin/activate
make db-init    # une seule fois (ou après modif du schéma)
make dev        # http://localhost:8000
```

### Imports de modules numérotés
Les dossiers de modules utilisent des underscores (`01_journal`) car Python n'accepte pas les tirets dans les noms de packages. L'import se fait via `importlib` :
```python
import importlib
mod = importlib.import_module("src.modules.01_journal.routes")
```

### Templates Jinja2
Centralisés dans `src/templating.py` (évite les imports circulaires). Import à faire depuis ce module :
```python
from src.templating import templates
```

### Migrations DB
Les colonnes ajoutées après la création initiale sont gérées dans `src/db/connection.py` (fonctions `_migrate_*`). Pas de système de migration complexe.

### Dépôt
- Local : `~/Programmation/sources/compagnon-de-jardin`
- GitHub : `git@github.com:brsjrn/compagnon-de-jardin.git`

---

## Historique des sessions

| Date | Action |
|---|---|
| 2026-07-14 | Création du projet. Structuration initiale. Rédaction de CONTEXTE.md. |
| 2026-07-14 | **Étape 0 terminée.** FastAPI + Jinja2 + HTMX + SQLite opérationnels. Schéma DB créé (9 tables). |
| 2026-07-15 | **Module 01 terminé.** CRUD interventions/observations/parcelles. Interface HTMX à 3 onglets, filtres, pagination. |
| 2026-07-15 | **Module 02 terminé.** Recherche Wikipedia (API REST), cache local, catalogue de variétés, import Wikipedia→catalogue. |
| 2026-07-15 | **Module 03 terminé.** Calendrier Gantt annuel, planification par parcelles, rotations, workflow statuts. |

---

*Fin du fichier. Si tu es un LLM, passe à l'action décrite dans « Prochaine action ».*
