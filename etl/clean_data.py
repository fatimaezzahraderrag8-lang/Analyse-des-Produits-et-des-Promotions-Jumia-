import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from utils.fonction_outlier import remove_outliers
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
    df = pd.read_sql(
        "SELECT * FROM staging.products_raw",
        engine
    )
    print("Lecture staging terminée.")
    # Nettoyage prix
    for col in ["new_price", "old_price"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("EGP","",regex=False)
            .str.replace("DH","",regex=False)
            .str.replace(",","",regex=False)
            .str.replace(" ","",regex=False)
        )
    # Pourcentage
    for col in ["percent_discount","saler_score"]:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace("%","",regex=False)
        )
    # Numeric conversion
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
        df[col] = df[col].fillna(
            df[col].median()
        )
    # Remove duplicates
    df = df.drop_duplicates()
    # Outliers
    for col in numeric_columns:

        df = remove_outliers(
            df,
            col
        )
    # Create clean schema
    with engine.connect() as conn:

        conn.execute(
            text("CREATE SCHEMA IF NOT EXISTS clean")
        )
        conn.commit()
    df.to_sql(
        "products_clean",
        schema="clean",
        con=engine,
        if_exists="replace",
        index=False
    )
    print("Cleaning terminé.")
    return df
if __name__ == "__main__":
    clean_data()