# core/db.py

from sqlmodel import create_engine, Session, SQLModel
# 1. Importamos la variable DATABASE_URL desde nuestro nuevo archivo de config
from core.config import DATABASE_URL 

# 2. Usamos la variable importada para crear el engine
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """
    Crea la base de datos y todas las tablas definidas con SQLModel.
    Se debe llamar al iniciar la aplicación.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Función de dependencia que proporciona una sesión de base de datos
    para cada petición.
    """
    with Session(engine) as session:
        yield session