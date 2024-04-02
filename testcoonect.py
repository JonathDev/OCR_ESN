import urllib
from sqlalchemy import create_engine

# Informations de connexion (remplacez par vos propres valeurs)
server = 'ocr-serveur-jonathan.database.windows.net'
database = 'db-ocr-jonathan'
username = 'ocrjonathan'
password = '2Alariszera!'
driver = '{ODBC Driver 18 for SQL Server}'

# Encode les informations de connexion
params = urllib.parse.quote_plus(f"DRIVER={driver};SERVER=tcp:{server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;")

# Crée l'engine SQLAlchemy
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Teste la connexion
try:
    with engine.connect() as connection:
        print("Connexion réussie !")
except Exception as e:
    print(f"Erreur lors de la connexion à la base de données: {e}")