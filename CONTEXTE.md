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
- [x] Initialisation Git

### En cours
- [ ] Étape 0 — Socle technique (démarrage du projet)

### À faire (priorisé)
1. **Module 01 — Journal de culture** : saisie et consultation des interventions, récoltes, observations
2. **Module 02 — Base de connaissances** : fiches variétés, parcelles, agrégation de sources externes (Wikipedia, etc.)
3. **Module 03 — Planification** : calendrier, rotations, aide au choix des variétés
4. **Module 04 — Capteurs** : données météo (API open data), puis capteurs locaux
5. **Module 05 — Assistant IA** : interface conversationnelle (Deepseek) avec contexte du jardin

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
│   ├── db/
│   │   ├── schema.sql       ← Schéma SQLite (DDL)
│   │   └── connection.py    ← Connexion et helpers DB
│   ├── modules/
│   │   ├── 01-journal/      ← Module B originel — mémoire du jardin
│   │   ├── 02-connaissances/← Module D originel — savoirs externes + personnels
│   │   ├── 03-planification/← Module A originel — projections, calendrier
│   │   ├── 04-capteurs/     ← Module C originel — données environnementales
│   │   └── 05-assistant/    ← Module E originel — IA conversationnelle (Deepseek)
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

> **Créer le socle technique (Étape 0) : initialiser l'environnement Python, vérifier que FastAPI démarre, créer le schéma de base, faire le premier commit.**

---

## Historique des sessions

| Date | Action |
|---|---|
| 2026-07-14 | Création du projet. Structuration initiale. Rédaction de CONTEXTE.md. |

---

*Fin du fichier. Si tu es un LLM, passe à l'action décrite dans « Prochaine action ».*
