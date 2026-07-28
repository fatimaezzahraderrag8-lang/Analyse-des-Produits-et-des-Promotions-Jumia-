import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

def load_staging(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    df = pd.read_csv(file_path)

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")

    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname="postgres"
    )

    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname=%s",
        (db,)
    )

    if cursor.fetchone() is None:
        cursor.execute(f'CREATE DATABASE "{db}"')

    cursor.close()
    conn.close()

    DATABASE_URL = (
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    )

    engine = create_engine(DATABASE_URL)

    with engine.begin() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS staging"))

    df.to_sql(
        "products_raw",
        con=engine,
        schema="staging",
        if_exists="replace",
        index=False,
        method="multi"
    )

    print("Chargement staging terminé.")


if __name__ == "__main__":
    load_staging("/opt/airflow/data/raw/jumia_products.csv")