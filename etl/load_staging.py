import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Charger les variables d'environnement
load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

# Charger le fichier CSV
df = pd.read_csv(r"C:\data pipeline et bi fil rouge\data\raw\jumia_products.csv")

try:
    # Connexion à PostgreSQL (base postgres)
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname="postgres"
    )

    conn.autocommit = True
    cursor = conn.cursor()

    # Vérifier si la base existe
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s;",
        (db,)
    )

    if cursor.fetchone() is None:
        cursor.execute(f'CREATE DATABASE "{db}"')
        print(f"Base de données '{db}' créée.")
    else:
        print(f"Base de données '{db}' existe déjà.")

    cursor.close()
    conn.close()

    # Connexion à la nouvelle base
    DATABASE_URL = (
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    )

    engine = create_engine(DATABASE_URL)

    print("Connexion OK")

    # Création du schéma staging
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging"))
        conn.commit()

    print("Schéma staging prêt")

    # Chargement des données
    df.to_sql(
        name="products_raw",
        con=engine,
        schema="staging",
        if_exists="replace",   # replace la première fois si tu veux recréer la table
        index=False
    )

    print("Données chargées")

except Exception as e:
    print(" Erreur :", e)