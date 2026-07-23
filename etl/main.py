from etl.extract import extract_data
from etl.load_staging import load_staging
from etl.clean_data import clean_data
from etl.transform import transform
if __name__ == "__main__":
    print("START ETL PIPELINE")
    file_path = "data/raw/jumia_products.csv"
    # Extract
    df = extract_data(file_path)
    # Load staging
    load_staging(df)
    # Clean
    clean_data()
    # Transform
    transform()
    print("ETL PIPELINE TERMINE")