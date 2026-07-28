import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Chargement des variables d'environnement
load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)


def load_datawarehouse():

    # Lecture de la table clean
    df = pd.read_sql(
        "SELECT * FROM clean.products_clean",
        engine
    )

    print("Lecture de clean.products_clean terminée.")

    # Vider les tables
    with engine.begin() as conn:

        conn.execute(text("""
            TRUNCATE TABLE dw.fact_products RESTART IDENTITY CASCADE;
        """))

        conn.execute(text("""
            TRUNCATE TABLE dw.dim_product RESTART IDENTITY CASCADE;
        """))

        conn.execute(text("""
            TRUNCATE TABLE dw.dim_vendor RESTART IDENTITY CASCADE;
        """))

        conn.execute(text("""
            TRUNCATE TABLE dw.dim_quality RESTART IDENTITY CASCADE;
        """))

    print("Anciennes données supprimées.")

    # DIM_PRODUCT
    dim_product = (
        df[["name", "price_category"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim_product.to_sql(
        "dim_product",
        engine,
        schema="dw",
        if_exists="append",
        index=False
    )

    print("dim_product chargée.")

    # Récupération des IDs
    product_db = pd.read_sql(
        "SELECT * FROM dw.dim_product",
        engine
    )

    # DIM_VENDOR
    dim_vendor = (
        df[["seller_level", "saler_score", "Followers"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim_vendor.columns = [
        "seller_level",
        "saler_score",
        "followers"
    ]

    dim_vendor.to_sql(
        "dim_vendor",
        engine,
        schema="dw",
        if_exists="append",
        index=False
    )

    print("dim_vendor chargée.")

    seller_db = pd.read_sql(
        "SELECT * FROM dw.dim_vendor",
        engine
    )

    # DIM_QUALITY
    dim_quality = (
        df[
            [
                "Quality Score",
                "Customer Rating",
                "Order Fulfillment_Rate"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim_quality.columns = [
        "quality_score",
        "customer_rating",
        "order_fulfillment_rate"
    ]

    dim_quality.to_sql(
        "dim_quality",
        engine,
        schema="dw",
        if_exists="append",
        index=False
    )

    print("dim_quality chargée.")

    quality_db = pd.read_sql(
        "SELECT * FROM dw.dim_quality",
        engine
    )

    # Construction de la table de fact
    fact = df.merge(
        product_db,
        on=["name", "price_category"]
    )

    fact = fact.merge(
        seller_db,
        left_on=[
            "seller_level",
            "saler_score",
            "Followers"
        ],
        right_on=[
            "seller_level",
            "saler_score",
            "followers"
        ]
    )

    fact = fact.merge(
        quality_db,
        left_on=[
            "Quality Score",
            "Customer Rating",
            "Order Fulfillment_Rate"
        ],
        right_on=[
            "quality_score",
            "customer_rating",
            "order_fulfillment_rate"
        ]
    )

    fact_products = fact[
        [
            "product_id",
            "seller_id",
            "quality_id",
            "new_price",
            "old_price",
            "percent_discount",
            "discount_amount",
            "rate",
            "verified_ratings",
            "popularity",
            "is_discounted"
        ]
    ]

    fact_products.to_sql(
        "fact_products",
        engine,
        schema="dw",
        if_exists="append",
        index=False
    )

    print("fact_products chargée.")
    print("Data Warehouse chargé avec succès.")


if __name__ == "__main__":
    load_datawarehouse()