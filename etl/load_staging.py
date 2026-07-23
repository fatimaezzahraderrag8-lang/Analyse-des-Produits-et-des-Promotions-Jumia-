import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Charger les variables d'environnement
load_dotenv()


def load_staging(df):
    """
    Crée la base de données si elle n'existe pas,
    crée le schéma staging et charge les données.
    """

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")

    try:
        # Connexion à la base postgres
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

        # Connexion à la base du projet
        DATABASE_URL = (
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
        )

        engine = create_engine(DATABASE_URL)

        print("Connexion PostgreSQL OK")

        # Création du schéma staging
        with engine.begin() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging"))

        print("Schéma staging prêt")

        # Chargement des données
        df.to_sql(
            name="products_raw",
            schema="staging",
            con=engine,
            if_exists="replace",
            index=False
        )

        print("Données chargées dans staging.products_raw")

    except Exception as e:
        print("Erreur :", e)
        raise


if __name__ == "__main__":

    file_path = r"C:\data pipeline et bi fil rouge\data\raw\jumia_products.csv"

    df = pd.read_csv(file_path)

    load_staging(df)