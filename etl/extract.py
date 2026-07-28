import os
import pandas as pd

def extract_data(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    df = pd.read_csv(file_path)

    print(df.head())

    print(f"Nombre de lignes : {len(df)}")

    return file_path

if __name__ == "__main__":

    extract_data("/opt/airflow/data/raw/jumia_products.csv")