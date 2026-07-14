# Questions ouvertes

> Fichier vivant. On note ici ce qui n'est pas encore tranché, pour y revenir plus tard avec plus de données.

---

## Architecture & Technique

- [ ] **Interface mobile** : PWA ou app native légère (F-Droid) ? La PWA suffit-elle pour la saisie vocale et les photos au jardin ?
- [ ] **Mode hors-ligne** : jusqu'où va le off-line ? Synchronisation différée ou full-local avec backup ?
- [ ] **Sauvegarde** : stratégie de backup de `data/compagnon.db` ? Simple copie ? Git LFS ? Nextcloud auto-sync ?
- [ ] **Multi-utilisateur** : le système doit-il gérer plusieurs jardiniers (famille) ou rester mono-utilisateur ?

---

## Connaissances

- [ ] **Sources de connaissances** : au-delà de Wikipedia, quelles sources pour les données agronomiques pratiques ? Tela Botanica ? GNIS ? INRAE ? Base de données open source type Open Food Facts pour le jardin ?
- [ ] **Cache des données externes** : quelle stratégie ? Extraction périodique ? À la demande avec TTL ? Full mirror local ?
- [ ] **Fiches variétés** : template standard à définir. Quels champs obligatoires ?

---

## Jardin

- [ ] **Sol argileux** : quelles cultures sont adaptées ? Faut-il amender avant la première saison ?
- [ ] **Préparation du terrain** : buttes, planches, lasagnes, permaculture ? La méthode influence la modélisation des parcelles.
- [ ] **Eau** : récupération d'eau de pluie ? Arrosage manuel ou semi-automatisé ?
- [ ] **Démarrage Année 1** : quand ? Printemps 2027 ? Automne 2026 pour préparer le sol ?

---

## Capteurs & Matériel

- [ ] **Capteurs** : lesquels sont réellement utiles en Année 1 vs. Année 3 ? Thermomètre + pluviomètre manuel suffisent probablement au début.
- [ ] **Microcontrôleur** : ESP32 ? Arduino ? Raspberry Pi dédié au jardin ?
- [ ] **Alimentation** : solaire + batterie pour les capteurs distants ?

---

## IA & Assistant

- [ ] **RAG ou fine-tuning** : pour l'assistant, un simple RAG sur les données du jardin suffit-il, ou faudra-t-il un jour fine-tuner un modèle ?
- [ ] **Modèle local** : à quel moment un modèle local (Ollama, llama.cpp) devient-il préférable à l'API Deepseek ? (coût, vie privée, résilience)
- [ ] **Prompt système** : comment formuler le prompt pour que l'assistant explicite son raisonnement et reste humble ?

---

*Dernière mise à jour : 2026-07-14*
