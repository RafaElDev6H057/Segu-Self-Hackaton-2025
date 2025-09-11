# models/advertencia.py

from typing import Optional
from sqlmodel import Field, SQLModel

class Advertencia(SQLModel, table=True):
    """
    Representa la tabla 'advertencia' en la base de datos.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    categoria: str = Field(index=True, max_length=50)
    descripcion: str
    nivel_advertencia: str = Field(max_length=10)