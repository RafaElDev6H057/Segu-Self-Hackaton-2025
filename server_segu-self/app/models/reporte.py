# models/reporte.py

from typing import Optional, TYPE_CHECKING
from datetime import date, time, datetime
from sqlmodel import Field, SQLModel, Relationship

# Esto previene errores de importación circular
if TYPE_CHECKING:
    from .user import User

class Reporte(SQLModel, table=True):
    """
    Representa la tabla 'reporte' en la base de datos.
    Ahora incluye una relación con la tabla 'user'.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    
    fecha: date = Field(default_factory=date.today, nullable=False)
    hora: time = Field(default_factory=lambda: datetime.now().time(), nullable=False)

    ubicacion: str = Field(max_length=255)
    tipo_evento: str = Field(index=True, max_length=50)
    nivel_gravedad: str = Field(max_length=20)
    descripcion: str
    
    # --- NUEVA RELACIÓN ---
    # Esta columna contendrá el ID del usuario que creó el reporte.
    usuario_id: int = Field(foreign_key="user.id")
    
    # Este atributo crea la relación para poder acceder al objeto User completo.
    # back_populates debe coincidir con el nombre del atributo en el modelo User.
    usuario: "User" = Relationship(back_populates="reportes")