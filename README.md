# Compagnon de jardin

> Système hybride (jardinage + numérique + IA) pour accompagner la création et l'évolution d'un potager nourricier.

Objectif : réduire la charge mentale du jardinier sans remplacer son jugement, sa sensibilité, ni son observation directe.

---

## Démarrage rapide

```bash
# Installer les dépendances
pip install -e .

# Initialiser la base de données
make db-init

# Lancer le serveur
make run
```

Puis ouvrir http://localhost:8000

---

## Principes

- **Frugalité** : chaque ligne de code justifie son existence
- **Progressivité** : commencer simple, ajouter des briques chaque année
- **Résilience** : le potager fonctionne sans le numérique
- **Apprentissage** : le système aide le jardinier à comprendre, pas à exécuter
- **Libre** : formats ouverts, logiciels libres, pas de dépendance propriétaire

---

## Documentation

| Fichier | Pour qui | Pour quoi |
|---|---|---|
| `CONTEXTE.md` | LLM + humain | Tableau de bord, état courant, prochaine action |
| `MANIFESTE.md` | Tout le monde | Intention fondatrice |
| `CAHIER_DES_CHARGES.md` | Contributeurs | Périmètre complet du projet |
| `QUESTIONS_OUVERTES.md` | Équipe | Points à trancher plus tard |
| `docs/architecture.md` | Développeurs | Architecture logicielle détaillée |
| `docs/decisions.md` | Développeurs | Registre des décisions (ADR) |

---

## Licence

À définir.
