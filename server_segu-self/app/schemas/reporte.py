# schemas/reporte.py

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date, time
from enum import Enum

# Importamos el schema público de usuario para anidarlo en la respuesta
from .user import UserPublic 

# --- Enums (sin cambios) ---
class TipoEvento(str, Enum):
    DELITO = "Delito"
    ACCIDENTE = "Accidente"
    DESASTRE_NATURAL = "Desastre Natural"
    INCENDIO = "Incendio"
    OTRO = "Otro"

class NivelGravedad(str, Enum):
    LEVE = "Leve"
    MODERADO = "Moderado"
    GRAVE = "Grave"
    CRITICO = "Crítico"

# --- Esquema Base (sin cambios) ---
class ReporteBase(BaseModel):
    ubicacion: str = Field(..., max_length=255)
    tipo_evento: TipoEvento
    nivel_gravedad: NivelGravedad
    descripcion: str

# --- Esquema para la Creación (MODIFICADO) ---
# Ahora solicita el email del usuario que crea el reporte.
class ReporteCreate(ReporteBase):
    usuario_email: EmailStr = Field(..., description="Email del usuario que crea el reporte.")

# --- Esquema para la Actualización (sin cambios) ---
class ReporteUpdate(BaseModel):
    ubicacion: Optional[str] = None
    tipo_evento: Optional[TipoEvento] = None
    nivel_gravedad: Optional[NivelGravedad] = None
    descripcion: Optional[str] = None

# --- Esquema Público (MODIFICADO) ---
# El modelo que se devolverá al cliente.
class ReportePublic(ReporteBase):
    id: int
    fecha: date
    hora: time
    # --- NUEVO ---
    # Este campo mostrará los datos del usuario que creó el reporte.
    usuario: UserPublic 

    class Config:
        from_attributes = True