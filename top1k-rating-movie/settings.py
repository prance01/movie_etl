import os 

# directory 
DATA_FOLDER = os.getenv('DATA_FOLDER')

# database setting
DB_ACCOUNT = os.getenv('DB_ACCOUNT')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_SCHEMA = os.getenv('DB_SCHEMA')
DB_TABLE = os.getenv('DB_TABLE')

DB_URI = f"postgresql+psycopg2://{DB_ACCOUNT}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_SCHEMA}"
 