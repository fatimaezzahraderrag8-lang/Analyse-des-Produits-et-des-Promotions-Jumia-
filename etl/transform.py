import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
# Import des fonctions de Feature Engineering
from utils.fonction_feauture_engineering import (
    price_category,
    popularity,
    seller_level
)
# Chargement des variables d'environnement
load_dotenv()
# Connexion à PostgreSQL
DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)
engine = create_engine(DATABASE_URL)
def transform():
    # Lecture des données depuis la table clean
    df = pd.read_sql(
        "SELECT * FROM clean.products_clean",
        engine
    )
    print("Lecture des données depuis clean.products_clean terminée.")
    # Feature Engineering
    # Création de nouvelles variables utiles
    # Calcul du montant de la réduction
    df["discount_amount"] = (
        df["old_price"] -
        df["new_price"]
    ).clip(lower=0)
    # Identifier si le produit est en promotion
    df["is_discounted"] = df["percent_discount"].apply(
        lambda x: "Yes" if x > 0 else "No"
    )
    # Catégorie du produit selon son prix
    df["price_category"] = df["new_price"].apply(
        price_category
    )
    # Niveau de popularité selon les avis clients
    df["popularity"] = df["verified_ratings"].apply(
        popularity
    )
    # Classification du vendeur selon son score
    df["seller_level"] = df["saler_score"].apply(
        seller_level
    )
    # Sauvegarde dans la même table clean
    # Remplacement de l'ancienne version
    df.to_sql(
        name="products_clean",
        schema="clean",
        con=engine,
        if_exists="replace",
        index=False
    )
    print(
        "Transformation terminée avec succès."
    )
    return df
# Exécution directe du fichier
if __name__ == "__main__":
    transform()