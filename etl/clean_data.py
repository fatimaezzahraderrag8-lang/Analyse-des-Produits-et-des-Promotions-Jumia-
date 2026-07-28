import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from utils.fonction_outlier import remove_outliers

# Charger les variables environnement
load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

def clean_data():
    # Lecture depuis staging
    df = pd.read_sql(
        "SELECT * FROM staging.products_raw",
        engine
    )
    print("Lecture staging terminée.")

    # Nettoyage des prix
    for col in ["new_price", "old_price"]:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace("EGP", "", regex=False)
            .str.replace("DH", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace(" ", "", regex=False)
        )

    # Nettoyage pourcentage
    for col in ["percent_discount", "saler_score"]:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace("%", "", regex=False)
        )

    # Conversion numérique
    numeric_columns = [
        "new_price",
        "old_price",
        "percent_discount",
        "rate",
        "verified_ratings",
        "saler_score",
        "Followers"
    ]

    for col in numeric_columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # Remplacer valeurs manquantes numériques
    for col in numeric_columns:

        df[col] = df[col].fillna(
            df[col].median()
        )

    # Remplacer valeurs manquantes texte
    text_columns = [
        "name",
        "Order Fulfillment_Rate",
        "Quality Score",
        "Customer Rating"
    ]

    for col in text_columns:

        if col in df.columns:

            df[col] = df[col].fillna(
                df[col].mode()[0]
            )

    # Suppression doublons
    df = df.drop_duplicates()
    print("Doublons supprimés.")

    # Suppression Outliers
    for col in numeric_columns:

        df = remove_outliers(
            df,
            col
        )
    print("Outliers traités.")

    # Création schema clean
    with engine.begin() as conn:

        conn.execute(
            text(
                "CREATE SCHEMA IF NOT EXISTS clean"
            )
        )

    # Chargement table clean
    df.to_sql(
        name="products_clean",
        schema="clean",
        con=engine,
        if_exists="replace",
        index=False
    )
    print("Données chargées dans clean.products_clean")
    return df
if __name__ == "__main__":
    clean_data()