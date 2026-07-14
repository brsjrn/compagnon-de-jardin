-- Schéma initial de la base de données
-- Module 01 — Journal de culture (tables principales)

-- Parcelles du jardin
CREATE TABLE IF NOT EXISTS parcelles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    surface_m2 REAL,
    exposition TEXT,          -- nord, sud, est, ouest, mixte
    type_sol TEXT,            -- argileux, sableux, limoneux, amendé
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Variétés cultivées (fiches personnelles)
CREATE TABLE IF NOT EXISTS varietes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    nom_latin TEXT,
    type TEXT,                -- légume, fruit, aromatique, fleur, engrais_vert
    famille TEXT,             -- solanacées, cucurbitacées, fabacées, etc.
    description TEXT,
    source TEXT DEFAULT 'personnel',   -- wikipedia, personnel, autre
    wiki_title TEXT,                   -- titre de l'article Wikipedia associé
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Saisons de culture (une occurrence = une culture sur une parcelle pendant une période)
CREATE TABLE IF NOT EXISTS cultures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parcelle_id INTEGER NOT NULL,
    variete_id INTEGER NOT NULL,
    date_semis DATE,
    date_plantation DATE,
    date_premiere_recolte DATE,
    date_arrachage DATE,
    quantite_plantee INTEGER, -- nombre de plants
    rendement_kg REAL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parcelle_id) REFERENCES parcelles(id),
    FOREIGN KEY (variete_id) REFERENCES varietes(id)
);

-- Interventions (actions réalisées au jardin)
CREATE TABLE IF NOT EXISTS interventions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_intervention DATE NOT NULL,
    type TEXT NOT NULL,       -- semis, plantation, arrosage, desherbage, paillage, taille, traitement, recolte, autre
    parcelle_id INTEGER,
    culture_id INTEGER,
    description TEXT NOT NULL,
    duree_minutes INTEGER,   -- temps passé
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parcelle_id) REFERENCES parcelles(id),
    FOREIGN KEY (culture_id) REFERENCES cultures(id)
);

-- Récoltes (détaillées)
CREATE TABLE IF NOT EXISTS recoltes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_recolte DATE NOT NULL,
    culture_id INTEGER NOT NULL,
    quantite_kg REAL,
    qualite TEXT,             -- excellent, bon, moyen, mauvais
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (culture_id) REFERENCES cultures(id)
);

-- Observations libres (notes, photos, incidents, météo ressentie)
CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_observation DATE NOT NULL,
    type TEXT NOT NULL,       -- observation, incident, meteo, photo, note_vocale
    parcelle_id INTEGER,
    description TEXT NOT NULL,
    chemin_fichier TEXT,      -- chemin relatif vers photo ou audio
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parcelle_id) REFERENCES parcelles(id)
);

-- Données météo (historique et prévisions, stockées localement)
CREATE TABLE IF NOT EXISTS meteo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    temperature_min REAL,
    temperature_max REAL,
    precipitation_mm REAL,
    humidite_pc REAL,
    vent_kmh REAL,
    source TEXT DEFAULT 'api_open_meteo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Données de capteurs locaux (futur module 04)
CREATE TABLE IF NOT EXISTS capteurs_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP NOT NULL,
    capteur_id TEXT NOT NULL,
    type_mesure TEXT NOT NULL, -- temperature_sol, humidite_sol, temperature_air, pluviometrie
    valeur REAL NOT NULL,
    unite TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cache Wikipedia (pour éviter les appels API répétés)
CREATE TABLE IF NOT EXISTS wiki_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    lang TEXT NOT NULL DEFAULT 'fr',
    extract TEXT,
    extract_html TEXT,
    thumbnail_url TEXT,
    page_url TEXT,
    raw_json TEXT,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index pour les requêtes fréquentes
CREATE INDEX IF NOT EXISTS idx_interventions_date ON interventions(date_intervention);
CREATE INDEX IF NOT EXISTS idx_observations_date ON observations(date_observation);
CREATE INDEX IF NOT EXISTS idx_cultures_parcelle ON cultures(parcelle_id);
CREATE INDEX IF NOT EXISTS idx_recoltes_date ON recoltes(date_recolte);
CREATE INDEX IF NOT EXISTS idx_meteo_date ON meteo(date);
CREATE INDEX IF NOT EXISTS idx_wiki_cache_title ON wiki_cache(title);
