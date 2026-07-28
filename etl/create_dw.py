# charge bibliotique
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
# Charger les variables d'environnement
load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

with engine.begin() as conn:

    # Création du schéma
    conn.execute(text("""
        CREATE SCHEMA IF NOT EXISTS dw;
    """))

    # DIM_PRODUCT
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dw.dim_product (
            product_id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            price_category VARCHAR(50)
        );
    """))

    # DIM_VENDOR
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dw.dim_vendor (
            seller_id SERIAL PRIMARY KEY,
            seller_level VARCHAR(50),
            saler_score NUMERIC,
            followers NUMERIC
        );
    """))

    # DIM_QUALITY
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dw.dim_quality (
            quality_id SERIAL PRIMARY KEY,
            quality_score VARCHAR(50),
            customer_rating VARCHAR(50),
            order_fulfillment_rate VARCHAR(50)
        );
    """))

    # FACT_PRODUCTS
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dw.fact_products (

            fact_id SERIAL PRIMARY KEY,

            product_id INT REFERENCES dw.dim_product(product_id),

            seller_id INT REFERENCES dw.dim_vendor(seller_id),

            quality_id INT REFERENCES dw.dim_quality(quality_id),

            new_price NUMERIC,
            old_price NUMERIC,
            percent_discount NUMERIC,
            discount_amount NUMERIC,
            rate NUMERIC,
            verified_ratings NUMERIC,
            popularity VARCHAR(50),
            is_discounted BOOLEAN
        );
    """))

print("Data Warehouse créé avec succès.")