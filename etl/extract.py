import pandas as pd
def extract_data(file_path):
    """
    Extraction des données depuis le fichier CSV.
    """
    df = pd.read_csv(file_path)
    print("Extraction des données terminée avec succès.")
    print(f"Nombre de lignes : {len(df)}")
    print(f"Nombre de colonnes : {len(df.columns)}")
    return df
if __name__ == "__main__":
    file_path = "data/raw/jumia_products.csv"
    df = extract_data(file_path)
    print(df.head())