import os
from dotenv import load_dotenv

# Carga las variables del archivo .env en el entorno del sistema
load_dotenv()

# --- Lee las variables de la base de datos ---
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# --- NUEVA LÍNEA: Lee la variable de la API de Google ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Construye la URL de la base de datos
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"