
image(85).png

jumia_etl_pipeline.py
Python

clean_data.py
Python

create_dw.py
Python

extract.py
Python

load_staging.py
Python

load_warehouse.py
Python

transform.py
Python

docker-compose.yml
Fichier

Dockerfile
Fichier

requirements.txt
Document
correge les codes pour ajouter airflow 

Le problème ne vient probablement pas du DAG Airflow lui-même. D'après la capture, extract est en success, mais load_staging est en failed, ce qui signifie que le DAG fonctionne et qu'Airflow exécute bien les tâches. 


Le problème est dans load_staging.py.

1. Ajouter Airflow dans requirements.txt
Ton fichier requirements.txt ne contient pas Airflow. 


Ajoute à la fin :

apache-airflow==2.10.0
apache-airflow-providers-postgres
SQLAlchemy==2.0.36
2. Modifier le Dockerfile
Ajoute l'installation des dépendances :

FROM apache/airflow:2.10.0-python3.11

USER root

RUN apt-get update && \
    apt-get install -y gcc libpq-dev

USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
3. Modifier docker-compose.yml
Le dossier du projet doit être monté :

volumes:
  - ./dags:/opt/airflow/dags
  - ./etl:/opt/airflow/etl
  - ./utils:/opt/airflow/utils
  - ./data:/opt/airflow/data
  - ./.env:/opt/airflow/.env
Dans les variables d'environnement :

environment:
  AIRFLOW__CORE__LOAD_EXAMPLES: "False"
  PYTHONPATH: /opt/airflow
4. Corriger le DAG
Je te conseille d'utiliser les fonctions directement.

from airflow.decorators import dag, task
from datetime import datetime

from etl.extract import extract_data
from etl.load_staging import load_staging
from etl.clean_data import clean_data
from etl.transform import transform
from etl.load_warehouse import load_datawarehouse


@dag(
    dag_id="jumia_etl_pipeline",
    start_date=datetime(2026,1,1),
    schedule="@daily",
    catchup=False
)

def jumia_etl_pipeline():

    @task
    def extract():
        return extract_data("/opt/airflow/data/raw/jumia_products.csv")

    @task
    def staging(path):
        load_staging(path)

    @task
    def cleaning():
        clean_data()

    @task
    def transformation():
        transform()

    @task
    def warehouse():
        load_datawarehouse()

    file = extract()
    s = staging(file)
    c = cleaning()
    t = transformation()
    w = warehouse()

    s >> c >> t >> w

dag = jumia_etl_pipeline()
Ton DAG est déjà très proche de cette version. 


5. Le vrai problème est sûrement dans load_staging.py
Le code crée une base PostgreSQL puis essaie d'y écrire. 


Sous Docker Airflow, il est préférable de ne pas créer la base à chaque exécution.

Remplace cette partie :

conn = psycopg2.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    dbname="postgres"
)
par simplement :

DATABASE_URL = (
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
)

engine = create_engine(DATABASE_URL)

with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging"))
Puis :

df.to_sql(
    "products_raw",
    con=engine,
    schema="staging",
    if_exists="replace",
    index=False,
    method="multi",
)
6. Pour connaître l'erreur exacte
Dans Airflow :

Graph
↓
load_staging
↓
Logs
Copie ici tout le message d'erreur (Traceback), surtout les dernières lignes.

Sans ces logs, on ne peut pas savoir si l'erreur est liée à :

PostgreSQL (connection refused)

.env introuvable

ModuleNotFoundError

No module named utils

FileNotFoundError

Permission denied

ou un autre problème.

Envoie également ton docker-compose.yml et le log complet de load_staging. Avec ces deux éléments, je pourrai te donner la version corrigée complète du projet Airflow.


ممتاز 👍

سنبني المشروع خطوة بخطوة حتى يعمل بدون أخطاء. في الرسالة الأولى سأعطيك الملفات الأساسية.

1. Dockerfile
FROM apache/airflow:2.10.0-python3.11

USER root

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev

USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
2. requirements.txt
apache-airflow==2.10.0
apache-airflow-providers-postgres==5.13.0

pandas==2.2.2
numpy==1.26.4

SQLAlchemy==1.4.53
psycopg2-binary==2.9.9

python-dotenv==1.0.1

matplotlib
3. .env
DB_HOST=postgres
DB_PORT=5432
DB_NAME=jumia_dw
DB_USER=postgres
DB_PASSWORD=postgres

AIRFLOW_DB_URL=postgresql+psycopg2://postgres:postgres@postgres:5432/airflow
4. docker-compose.yml
version: "3.9"

services:

  postgres:
    image: postgres:16

    container_name: postgres_dw

    restart: always

    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: jumia_dw

    ports:
      - "5432:5432"

    volumes:
      - postgres_data:/var/lib/postgresql/data

    healthcheck:
      test: ["CMD-SHELL","pg_isready -U postgres"]
      interval: 10s
      retries: 5

  airflow:

    build: .

    container_name: airflow

    depends_on:
      postgres:
        condition: service_healthy

    ports:
      - "8081:8080"

    environment:
      AIRFLOW_UID: 50000
      AIRFLOW__CORE__LOAD_EXAMPLES: "False"
      AIRFLOW__CORE__EXECUTOR: SequentialExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://postgres:postgres@postgres:5432/airflow
      PYTHONPATH: /opt/airflow

    volumes:
      - ./dags:/opt/airflow/dags
      - ./etl:/opt/airflow/etl
      - ./utils:/opt/airflow/utils
      - ./data:/opt/airflow/data
      - ./.env:/opt/airflow/.env
      - ./logs:/opt/airflow/logs

    command: >
      bash -c "
      airflow db migrate &&
      airflow users create
      --username admin
      --password admin
      --firstname Admin
      --lastname User
      --role Admin
      --email admin@gmail.com || true &&
      airflow standalone
      "

volumes:
  postgres_data:
بعد إنشاء هذه الملفات، نفذ:

docker compose down -v
docker compose build --no-cache
docker compose up -d
ثم أرسل لي كلمة "OK"، وسأرسل لك في الرسالة التالية:
✅ jumia_etl_pipeline.py

✅ extract.py

✅ load_staging.py

ثم بعد ذلك سأرسل ملفات:

clean_data.py

transform.py

create_dw.py

load_warehouse.py

حتى يصبح المشروع كاملاً ويعمل مع Airflow بدون أخطاء.


ok

ممتاز. نكمل الآن بالملفات الأساسية للـ DAG ومرحلتي Extract و Load Staging.

1. dags/jumia_etl_pipeline.py
from airflow.decorators import dag, task
from datetime import datetime

from etl.extract import extract_data
from etl.load_staging import load_staging
from etl.clean_data import clean_data
from etl.transform import transform
from etl.create_dw import create_dw
from etl.load_warehouse import load_datawarehouse


default_args = {
    "owner": "fatima",
    "retries": 1,
}


@dag(
    dag_id="jumia_etl_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
)

def jumia_etl_pipeline():

    @task
    def extract():
        return extract_data("/opt/airflow/data/raw/jumia_products.csv")

    @task
    def staging(file_path):
        load_staging(file_path)

    @task
    def cleaning():
        clean_data()

    @task
    def transforming():
        transform()

    @task
    def createwarehouse():
        create_dw()

    @task
    def warehouse():
        load_datawarehouse()

    file = extract()

    stage = staging(file)

    clean = cleaning()

    trans = transforming()

    dw = createwarehouse()

    wh = warehouse()

    stage >> clean >> trans >> dw >> wh


dag = jumia_etl_pipeline()
2. etl/extract.py
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
3. etl/load_staging.py
هذه النسخة لا تستعمل psycopg2.connect() نهائياً، وتعتمد فقط على SQLAlchemy.

import os

import pandas as pd

from dotenv import load_dotenv

from sqlalchemy import create_engine, text


load_dotenv()


DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)


def load_staging(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    df = pd.read_csv(file_path)

    with engine.begin() as conn:

        conn.execute(
            text(
                "CREATE SCHEMA IF NOT EXISTS staging"
            )
        )

    df.to_sql(
        "products_raw",
        con=engine,
        schema="staging",
        if_exists="replace",
        index=False,
        method="multi"
    )

    print("Chargement staging terminé")


if __name__ == "__main__":

    load_staging("/opt/airflow/data/raw/jumia_products.csv")
بعد حفظ هذه الملفات
نفذ:

docker compose down -v
ثم:

docker compose build --no-cache
ثم:

docker compose up -d
في الرسالة التالية سأرسل لك:
✅ clean_data.py

✅ transform.py

✅ create_dw.py

✅ load_warehouse.py

وبعدها سيكون مشروع الـ ETL كاملاً وجاهزًا للتشغيل مع Airflow.


ok

ممتاز، نكمل الآن بالملفات المتبقية.

1. etl/clean_data.py
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

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

    df = df.drop_duplicates()

    df = df.dropna(how="all")

    df.columns = df.columns.str.lower().str.strip()

    df.to_sql(
        "products_clean",
        engine,
        schema="clean",
        if_exists="replace",
        index=False
    )

    print("Cleaning terminé")


if __name__ == "__main__":
    clean_data()
2. etl/transform.py
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)


def transform():

    df = pd.read_sql(
        "SELECT * FROM clean.products_clean",
        engine
    )

    if "price" in df.columns:
        df["price"] = (
            df["price"]
            .astype(str)
            .str.replace(",", "")
            .astype(float)
        )

    if "rating" in df.columns:
        df["rating"] = pd.to_numeric(
            df["rating"],
            errors="coerce"
        )

    df.to_sql(
        "products_transform",
        engine,
        schema="clean",
        if_exists="replace",
        index=False
    )

    print("Transformation terminée")


if __name__ == "__main__":
    transform()
3. etl/create_dw.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)


def create_dw():

    with engine.begin() as conn:

        conn.execute(text(
            "CREATE SCHEMA IF NOT EXISTS clean;"
        ))

        conn.execute(text(
            "CREATE SCHEMA IF NOT EXISTS dw;"
        ))

    print("Schemas créés")


if __name__ == "__main__":
    create_dw()
4. etl/load_warehouse.py
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

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

    df = pd.read_sql(
        "SELECT * FROM clean.products_transform",
        engine
    )

    df.to_sql(
        "fact_products",
        engine,
        schema="dw",
        if_exists="replace",
        index=False
    )

    print("Data Warehouse chargé")


if __name__ == "__main__":
    load_datawarehouse()
⚠️ يوجد خطأ منطقي في ترتيب الـ DAG
في النسخة السابقة كان الترتيب:

extract
↓
load_staging
↓
clean_data
↓
transform
↓
create_dw
↓
load_warehouse
لكن clean_data يكتب في schema clean، لذلك يجب إنشاء الـ schema قبل ذلك.

رتّب المهام هكذا:

extract
↓
load_staging
↓
create_dw
↓
clean_data
↓
transform
↓
load_warehouse
أي في ملف jumia_etl_pipeline.py اجعل آخر سطر:

stage >> dw >> clean >> trans >> wh
بدل:

stage >> clean >> trans >> dw >> wh
هذا التعديل سيمنع خطأ من نوع:

schema "clean" does not exist
بعد هذه التعديلات، أعد بناء المشروع:

docker compose down -v
docker compose build --no-cache
docker compose up -d
ثم افتح Airflow وشغّل الـ DAG من جديد. إذا ظهر أي خطأ جديد، أرسل الـ Logs الخاصة بالمهمة التي فشلت وسنحلها خطوة بخطوة.


Bibliothèque
/
jumia_etl_pipeline.py


from airflow.decorators import dag, task
from datetime import datetime

from etl.extract import extract_data
from etl.load_staging import load_staging
from etl.clean_data import clean_data
from etl.transform import transform
from etl.load_warehouse import load_datawarehouse


default_args = {
    "owner": "fatima",
    "retries": 1,
}


@dag(
    dag_id="jumia_etl_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
)

def jumia_etl_pipeline():

    @task
    def extract():
        return extract_data("/opt/airflow/data/raw/jumia_products.csv")

    @task
    def staging(file_path):
        load_staging(file_path)

    @task
    def clean():
        clean_data()

    @task
    def transform_task():
        transform()

    @task
    def warehouse():
        load_datawarehouse()

    file_path = extract()

    stage = staging(file_path)
    clean_step = clean()
    transform_step = transform_task()
    warehouse_step = warehouse()

    stage >> clean_step >> transform_step >> warehouse_step


dag = jumia_etl_pipeline()
