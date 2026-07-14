# Cahier des charges — Compagnon de jardin (v1)

## 1. Vision

Concevoir un système hybride, associant pratiques de jardinage, outils numériques et intelligence artificielle, dont l'objectif est d'accompagner la création et l'évolution d'un potager nourricier.

Le système doit réduire la charge mentale liée à la planification et au suivi du potager, tout en favorisant le développement progressif des connaissances, de l'autonomie et de la sensibilité du jardinier vis-à-vis de son écosystème.

L'objectif n'est pas d'automatiser le jardinage, mais de concevoir un **compagnon de jardin** capable d'assister les prises de décision sans se substituer au jugement humain.

---

## 2. Objectifs

À moyen terme (3 à 5 ans), le système devra permettre :

- produire une part significative de l'alimentation du foyer ;
- limiter le temps consacré au potager à un volume compatible avec une activité professionnelle ;
- réduire les oublis et les erreurs de planification ;
- documenter l'évolution du jardin année après année ;
- améliorer progressivement les recommandations grâce à l'expérience acquise.

---

## 3. Valeurs du projet

Le projet repose sur plusieurs principes fondamentaux.

### Frugalité

Le système doit privilégier les solutions simples.

Chaque composant doit justifier son existence par un gain réel.

L'ajout de technologie n'est jamais une fin en soi.

### Progressivité

Le système doit pouvoir commencer avec très peu de matériel.

Chaque année doit pouvoir ajouter une nouvelle brique sans remettre en cause les précédentes.

### Apprentissage

Le système doit permettre au jardinier d'apprendre.

Il ne doit pas masquer le fonctionnement du jardin.

Il doit au contraire favoriser l'observation, l'expérimentation et la compréhension.

### Résilience

Le potager doit continuer à fonctionner si :

- Internet est indisponible ;
- un capteur tombe en panne ;
- l'ordinateur est arrêté.

Les outils numériques doivent assister le jardin, jamais devenir indispensables.

### Logiciels libres et données ouvertes

Dans la mesure du possible :

- formats ouverts ;
- logiciels libres ;
- données exportables ;
- absence de dépendance à un fournisseur unique.

---

## 4. Périmètre

Le projet couvre :

- planification annuelle du potager ;
- suivi des cultures ;
- aide à la décision ;
- historique des interventions ;
- collecte de données environnementales ;
- capitalisation de l'expérience.

Le projet ne cherche pas, dans un premier temps, à :

- automatiser complètement l'arrosage ;
- piloter des robots ;
- remplacer l'observation humaine.

---

## 5. Architecture générale

Le système est constitué de plusieurs couches.

```
Potager
    ↓
Observations humaines
    ↓
Capteurs
    ↓
Base de données
    ↓
Moteur de connaissances
    ↓
Assistant IA
    ↓
Interface utilisateur
```

Chaque couche peut évoluer indépendamment.

---

## 6. Les modules

Les modules sont numérotés dans l'ordre de construction (dépendances progressives).

### Module 01 — Journal de culture

Le journal doit conserver :

- interventions
- récoltes
- observations
- photos
- incidents
- temps passé

Le journal constitue la mémoire du jardin. C'est le module fondateur du système.

### Module 02 — Base de connaissances

Elle rassemble :

- connaissances générales (agrégées depuis des sources externes)
- retours d'expérience personnels
- fiches variétés
- fiches parcelles (caractéristiques du sol, exposition, historique)

Cette base est le cœur du système. Elle ne réécrit pas la connaissance existante : elle la référence, la met en cache local, et la croise avec les observations personnelles.

### Module 03 — Planification

Entrées :

- surface
- exposition
- variétés
- objectifs alimentaires
- disponibilité du jardinier

Sorties :

- calendrier
- plan du potager
- estimation de charge
- rotations
- semis

### Module 04 — Données environnementales

Collecte de :

- pluie
- température
- humidité du sol
- météo
- éventuellement vent

Les données doivent être historisées.

### Module 05 — Assistant

L'assistant doit être capable de répondre à des questions comme :

> Que puis-je semer cette semaine ?

> Quelles tâches sont prioritaires ?

> Pourquoi mes courges ont-elles moins produit cette année ?

> Cette variété vaut-elle la peine d'être replantée ?

L'assistant ne prend pas les décisions.

Il explicite son raisonnement.

L'assistant suggère des recommandations, fait des rappels, met en perspective la situation, structure et hiérarchise la connaissance du système.

---

## 7. Intelligence artificielle

L'IA est utilisée comme :

- interface conversationnelle ;
- aide à l'analyse ;
- synthèse d'informations ;
- générateur d'hypothèses.

Elle ne constitue pas la source de vérité, mais se trouve à l'intersection entre observation humaine et connaissance théorique pour être utile et pertinente.

---

## 8. Itérations

### Année 1

Objectifs :

- premier potager (30 m², sol argileux) ;
- aide au choix des variétés ;
- première planification ;
- premières données météo ;
- premier journal ;
- tableau de bord ;
- prédictions ;
- recommandations automatiques.

Le but est d'apprendre.

### Année 2

Ajouts possibles :

- comparaison entre années ;
- estimation des rendements ;
- suivi des rotations ;
- optimisation de la planification.

### Année 3+

Ajouts possibles :

- station météo locale ;
- expérimentation de nouvelles cultures.

---

## 9. Critères de réussite

Le projet est réussi si, après plusieurs années :

- le temps consacré à la planification diminue ;
- les oublis deviennent rares ;
- les rendements augmentent ;
- le jardinier comprend mieux son jardin ;
- le système est utilisé avec plaisir.

---

## 10. Critères d'échec

Le projet est considéré comme dérivant si :

- la maintenance informatique dépasse le temps consacré au jardin ;
- le système devient incompréhensible ;
- le jardinier exécute passivement les recommandations ;
- les données sont collectées sans être réellement exploitées ;
- la technologie remplace l'observation directe.

---

## 11. Questions de recherche

Le projet constitue également une démarche exploratoire. Parmi les questions ouvertes :

- Comment représenter fidèlement la mémoire d'un jardin ?
- Quelle est la frontière pertinente entre automatisation et accompagnement ?
- Quelles données sont réellement utiles à la prise de décision ?
- Comment rendre explicites les raisonnements de l'assistant pour qu'ils soient discutables et pédagogiques ?
- Comment concevoir une IA qui aide à former le regard plutôt qu'à le remplacer ?
- Comment intégrer des savoirs issus de sources diverses (agronomie, permaculture, observations personnelles, météo, capteurs) sans les hiérarchiser artificiellement ?
