# 📊 Analyse des Produits et des Promotions Jumia

## 📖 Présentation du projet

Ce projet consiste à développer une solution complète de Business Intelligence permettant d'analyser les produits et les promotions de la plateforme Jumia. Il met en œuvre un pipeline ETL automatisé pour extraire, nettoyer, transformer et intégrer les données dans un Data Warehouse PostgreSQL selon un modèle en étoile (Star Schema). Les données sont ensuite visualisées à travers plusieurs tableaux de bord interactifs réalisés avec Power BI afin d'aider les décideurs à analyser les performances commerciales.

Le projet s'adresse principalement aux analystes de données, aux responsables marketing, aux responsables commerciaux et à toute personne souhaitant exploiter les données des produits Jumia pour faciliter la prise de décision.

L'objectif principal est de construire une plateforme BI complète, automatisée, reproductible et documentée permettant d'obtenir des indicateurs fiables sur les produits, les promotions, les vendeurs et la satisfaction client.

---

# 🎯 Problématique

Les plateformes e-commerce proposent des milliers de produits, de promotions et de vendeurs. Sans processus d'analyse automatisé, il devient difficile d'obtenir rapidement des indicateurs fiables permettant d'identifier les meilleures promotions, les produits les plus performants ou les vendeurs les plus actifs.

Ce projet répond à cette problématique en développant une chaîne complète d'intégration de données (ETL) permettant de nettoyer les données, de les organiser dans un Data Warehouse et de les visualiser dans Power BI afin de faciliter l'analyse et la prise de décision.

---

# 🚀 Fonctionnalités principales

- Extraire automatiquement les données des produits Jumia.
- Charger les données dans une base PostgreSQL.
- Nettoyer et transformer les données.
- Construire un Data Warehouse selon un Star Schema.
- Automatiser le pipeline ETL avec Apache Airflow.
- Générer des tableaux de bord interactifs avec Power BI.
- Analyser les prix, les promotions et les performances des vendeurs.
- Suivre les indicateurs clés de performance (KPI).

---

# 🏗️ Architecture du projet

Le projet suit une architecture BI classique composée de plusieurs étapes :

```
Dataset CSV
      │
      ▼
Extraction (Python)
      │
      ▼
Staging (Bronze)
      │
      ▼
Cleaning (Silver)
      │
      ▼
Transformation
      │
      ▼
Data Warehouse (Gold)
      │
      ▼
Power BI Dashboards
```

Le pipeline est entièrement orchestré avec Apache Airflow afin d'automatiser chaque étape du traitement.

---

# ⭐ Architecture du Data Warehouse

Le Data Warehouse est construit selon un modèle en étoile (Star Schema).

### Tables de dimensions

- DIM_PRODUCT
- DIM_SELLER
- DIM_PROMOTION

### Table de faits

- FACT_PRODUCT

Cette modélisation permet d'optimiser les analyses multidimensionnelles et les performances des requêtes SQL.

---

# 🛠️ Technologies utilisées

| Technologie | Utilisation |
|-------------|-------------|
| Python | Développement du pipeline ETL |
| Pandas | Nettoyage et transformation des données |
| PostgreSQL | Base de données relationnelle |
| SQLAlchemy | Connexion entre Python et PostgreSQL |
| Apache Airflow | Orchestration du pipeline ETL |
| Docker | Conteneurisation de l'environnement |
| Power BI | Création des tableaux de bord |
| Git | Gestion des versions |
| GitHub | Hébergement du projet |
| Jira | Gestion Agile du projet |

---

# 📂 Structure du projet

```
Analyse-des-Produits-et-des-Promotions-Jumia
│
├── dags
├── data
├── etl
├── sql
├── images
├── dashboards
├── requirements.txt
├── docker-compose.yml
├── README.md
└── .env
```

---

# ⚙️ Installation

## Cloner le dépôt

```bash
git clone https://github.com/fatimaezzahraderrag8-lang/Analyse-des-Produits-et-des-Promotions-Jumia.git
```

## Accéder au projet

```bash
cd Analyse-des-Produits-et-des-Promotions-Jumia
```

## Installer les dépendances

```bash
pip install -r requirements.txt
```

## Lancer Docker

```bash
docker compose up -d
```

## Créer le Data Warehouse

```bash
docker exec -it airflow_scheduler bash

python etl/create_dw.py
```

## Exécuter le pipeline

Depuis Airflow :

```
http://localhost:8081
```

Lancer le DAG :

```
jumia_etl_pipeline
```

---

# 📸 Gestion du projet avec Jira

<img width="1566" height="802" alt="Capture d&#39;écran 2026-08-04 103839" src="https://github.com/user-attachments/assets/0214c901-a3de-4389-8a42-3fb74c743066" />


Le projet a été développé selon une méthodologie Agile avec Jira.

Les principales étapes du projet sont :

- Analyse et compréhension des données
- Collecte et ingestion
- Nettoyage et transformation
- Conception du Data Warehouse
- Développement du pipeline ETL
- Analyse des KPI
- Création des dashboards Power BI
- Documentation finale

---

# 🔄 Pipeline ETL avec Apache Airflow

<img width="1907" height="942" alt="Capture d&#39;écran 2026-08-04 124143" src="https://github.com/user-attachments/assets/e108380d-4d0f-477a-b35d-dedcd4d68773" />


Le pipeline est composé de cinq tâches automatisées :

- Extract
- Load Staging
- Clean Data
- Transform
- Load Data Warehouse

Chaque tâche est exécutée automatiquement par Apache Airflow.

---

# ⭐ Modèle en étoile

<img width="1536" height="1024" alt="Architecture_schema_start_schema" src="https://github.com/user-attachments/assets/d3aaf25d-d474-4640-8d81-57427698895b" />


Le modèle en étoile relie les dimensions Produit, Vendeur et Promotion à la table de faits FACT_PRODUCT afin de faciliter les analyses décisionnelles.

---

# 🏛️ Architecture complète du projet

<img width="1280" height="853" alt="Architecture_projet" src="https://github.com/user-attachments/assets/fc6c92d7-08e4-4e2c-843f-4afb97eb7eac" />


Cette architecture présente l'ensemble du flux de données depuis le fichier source jusqu'aux tableaux de bord Power BI.

Les principales étapes sont :

- Source de données CSV
- Pipeline ETL
- Architecture Medallion
- Data Warehouse
- Star Schema
- Dashboards Power BI

---

# 📊 Dashboards Power BI

Le projet comprend cinq tableaux de bord interactifs permettant d'explorer les données sous différents angles.

---

## 📊 Dashboard 1 : Vue Générale

<img width="1320" height="854" alt="dashboard1" src="https://github.com/user-attachments/assets/46398c70-2b96-4d6b-b9b1-9722817c2ddf" />


Ce tableau de bord offre une vision globale des données.

### KPI

- Nombre total de produits
- Prix moyen
- Note moyenne
- Produits en promotion

### Visualisations

- Nombre de produits par catégorie
- Répartition des promotions
- Prix moyen par catégorie
- Top 10 produits

---

## 💰 Dashboard 2 : Analyse des Prix

<img width="1309" height="840" alt="dashboard2" src="https://github.com/user-attachments/assets/06382d2a-cbb2-4dbb-9c30-43f4bafe3d50" />


Ce dashboard permet d'étudier les prix des produits.

### KPI

- Prix moyen
- Prix maximum
- Prix minimum
- Réduction moyenne

### Visualisations

- Ancien prix vs nouveau prix
- Distribution des prix
- Prix moyen par catégorie
- Relation entre prix et note

---

## 🏷️ Dashboard 3 : Analyse des Promotions

<img width="1320" height="859" alt="dashboard3" src="https://github.com/user-attachments/assets/c284fb3f-dbde-4f02-90b0-180854b618fa" />


Cette page analyse les promotions proposées sur Jumia.

### KPI

- Produits en promotion
- Réduction moyenne
- Réduction maximale

### Visualisations

- Répartition des promotions
- Promotions par catégorie
- Réduction moyenne
- Relation réduction / prix

---

## ⭐ Dashboard 4 : Satisfaction Client

<img width="1313" height="852" alt="dashboard4" src="https://github.com/user-attachments/assets/cfe3d3b3-0297-4948-b314-92b7e823dd46" />


Cette page mesure la satisfaction des clients.

### KPI

- Note moyenne
- Avis vérifiés
- Produits bien notés

### Visualisations

- Note par catégorie
- Customer Rating
- Top produits
- Relation entre la note et le Customer Rating

---

## 👥 Dashboard 5 : Performance des Vendeurs

<img width="1318" height="852" alt="dashboard5" src="https://github.com/user-attachments/assets/5707e80c-6fa1-4655-b79c-2f621146f8d2" />


Cette page analyse les performances des vendeurs.

### KPI

- Nombre de vendeurs
- Score moyen
- Nombre total de followers

### Visualisations

- Nombre de vendeurs par niveau
- Nombre de followers
- Répartition des vendeurs
- Relation Followers / Score vendeur

---

# 👩‍💻 Ma contribution

Dans ce projet, j'ai réalisé l'ensemble des étapes de développement :

- Analyse des besoins
- Nettoyage des données
- Développement des scripts Python
- Création du pipeline ETL
- Conception du Data Warehouse
- Développement des scripts SQL
- Automatisation avec Apache Airflow
- Conteneurisation avec Docker
- Création des dashboards Power BI
- Gestion du projet avec Jira
- Documentation complète du projet

---

# ⚠ Difficultés rencontrées

## Gestion des connexions PostgreSQL

Des erreurs de connexion sont apparues entre Python et PostgreSQL lors de l'exécution du pipeline.

Solution :

- Vérification des variables d'environnement
- Configuration Docker
- Tests des connexions SQLAlchemy

---

## Automatisation avec Airflow

La configuration des DAGs et des dépendances a nécessité plusieurs ajustements.

Solution :

- Vérification des imports
- Tests des tâches indépendamment
- Correction des chemins d'accès

---

# 🔮 Améliorations futures

Dans une prochaine version, le projet pourra être enrichi par :

- Déploiement sur le Cloud
- Intégration d'un Data Lake
- Utilisation de Snowflake
- Mise en place de dbt
- Rafraîchissement automatique des dashboards
- Détection d'anomalies par Machine Learning
- Prédiction des ventes
- Ajout d'une API de consultation des données

---

# 📌 Conclusion

Ce projet met en œuvre une chaîne complète de traitement de données allant de l'extraction jusqu'à la visualisation. Grâce au pipeline ETL automatisé, au Data Warehouse modélisé en Star Schema, à Apache Airflow et aux tableaux de bord Power BI, il fournit une solution Business Intelligence robuste permettant d'analyser efficacement les produits, les promotions, les vendeurs et la satisfaction client afin d'améliorer la prise de décision.
