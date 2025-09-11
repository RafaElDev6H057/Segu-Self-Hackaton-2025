# models/user.py

from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

# Esto previene errores de importación circular
if TYPE_CHECKING:
    from .reporte import Reporte

class User(SQLModel, table=True):
    """
    Representa la tabla de usuarios en la base de datos.
    Ahora incluye una relación con la tabla 'reporte'.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    
    nombre: str = Field(index=True, max_length=50)
    apellido_paterno: str = Field(max_length=50)
    apellido_materno: Optional[str] = Field(default=None, max_length=50)
    edad: int
    direccion: str = Field(max_length=255)
    email: str = Field(unique=True, index=True, max_length=100)
    telefono: str = Field(max_length=15)
    hashed_password: str = Field(..., description="Contraseña hasheada, nunca guardar en texto plano")

    # --- NUEVA RELACIÓN ---
    # Un usuario puede tener una lista de reportes.
    # back_populates debe coincidir con el nombre del atributo en el modelo Reporte.
    reportes: List["Reporte"] = Relationship(back_populates="usuario")