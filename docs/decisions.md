# Registre des décisions architecturales (ADR)

Format inspiré de [Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

---

## ADR-001 — SQLite comme base de données unique

**Date :** 2026-07-14
**Statut :** Accepté

### Contexte
Le projet doit être frugal, résilient et fonctionner hors-ligne. Les données sont à l'échelle d'un potager familial (quelques milliers d'enregistrements par an).

### Décision
Utiliser SQLite comme seule base de données.

### Justification
- Zéro serveur, zéro configuration, zéro dépendance réseau
- Un fichier unique, facile à sauvegarder (copie de `data/compagnon.db`)
- Performance largement suffisante pour l'échelle du projet
- Cohérent avec les valeurs de frugalité et résilience
- Inclus dans la stdlib Python, pas de dépendance externe

### Conséquences
- Pas de scalabilité horizontale (non nécessaire)
- Pas de types avancés (JSON stocké en TEXT, pas de vectoriel natif)
- Les migrations doivent être gérées manuellement (scripts SQL)

---

## ADR-002 — Pas d'ORM, SQL direct

**Date :** 2026-07-14
**Statut :** Accepté

### Contexte
Il faut interagir avec SQLite. Les ORM Python (SQLAlchemy, Peewee, Django ORM) ajoutent une couche d'abstraction et de complexité.

### Décision
Utiliser `sqlite3` de la stdlib avec des helpers légers (`connection.py`).

### Justification
- Le schéma est simple et stable
- Un ORM masquerait le SQL, rendant le projet plus difficile à comprendre pour un LLM
- Moins de dépendances = plus de résilience
- Les requêtes sont lisibles et explicites

### Conséquences
- Pas de validation automatique des types (compensé par Pydantic au niveau API)
- Les jointures doivent être écrites manuellement
- Plus facile à déboguer et à auditer

---

## ADR-003 — FastAPI + Jinja2 + HTMX (pas de SPA)

**Date :** 2026-07-14
**Statut :** Accepté

### Contexte
L'interface doit être utilisable sur PC et smartphone, avec une interactivité légère (formulaires, mise à jour partielle, pas de rechargement complet).

### Décision
Rendu côté serveur (SSR) avec Jinja2, interactivité via HTMX, pas de framework JavaScript.

### Justification
- Le développeur est à l'aise avec HTML/CSS mais pas avec React/Vue
- HTMX permet de l'interactivité avec quasi aucun JavaScript
- Le SSR est plus simple à raisonner qu'une SPA + API découplée
- Cohérent avec la valeur de frugalité
- Les LLM maîtrisent très bien ce stack

### Conséquences
- Certaines interactions complexes seront plus verbeuses qu'en SPA
- Pas de state management côté client (pas nécessaire au vu du périmètre)

---

## ADR-004 — Modules numérotés dans l'ordre de construction

**Date :** 2026-07-14
**Statut :** Accepté

### Contexte
Le cahier des charges original utilisait des lettres arbitraires (A, B, C, D, E) pour désigner les modules, sans lien avec leur ordre de dépendance.

### Décision
Renommer et numéroter les modules de 01 à 05 selon l'ordre de construction (dépendances progressives).

| Nouveau | Ancien | Nom |
|---|---|---|
| 01 | B | Journal |
| 02 | D | Connaissances |
| 03 | A | Planification |
| 04 | C | Capteurs |
| 05 | E | Assistant |

### Justification
- Le préfixe numérique donne immédiatement l'ordre de lecture et de construction
- Facilité la compréhension pour un LLM qui découvre le projet
- Les dépendances forment un DAG sans cycle

### Conséquences
- Renumérotation éventuelle si l'ordre des dépendances change (peu probable)

---

## ADR-005 — Deepseek comme fournisseur IA principal

**Date :** 2026-07-14
**Statut :** Accepté

### Contexte
Le module 05 (Assistant) nécessite un LLM pour l'interface conversationnelle et l'analyse.

### Décision
Utiliser Deepseek via son API compatible OpenAI SDK.

### Justification
- Coût très inférieur à OpenAI pour une qualité comparable
- L'utilisateur l'utilise déjà et en est satisfait
- API compatible avec la librairie `openai` (pas de wrapper spécifique)
- Possibilité de migrer vers un modèle local (Ollama) plus tard sans changer l'architecture

### Conséquences
- Dépendance à un fournisseur externe (contredit partiellement la valeur de résilience)
- Atténué par : l'assistant est le dernier module, optionnel, et le jardin fonctionne sans lui
- Un fallback vers un modèle local est prévu dans les questions ouvertes

---

*Dernière mise à jour : 2026-07-14*
