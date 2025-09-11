# schemas/advertencia.py

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

# Definimos los niveles de advertencia permitidos usando un Enum
class NivelAdvertencia(str, Enum):
    BAJO = "Bajo"
    MEDIO = "Medio"
    ALTO = "Alto"

# --- Esquema Base ---
# Contiene los campos comunes que se usan al crear y leer.
class AdvertenciaBase(BaseModel):
    categoria: str = Field(..., max_length=50, description="Categoría de la advertencia (ej. 'Seguridad', 'Rendimiento')")
    descripcion: str = Field(..., description="Descripción detallada de la advertencia")
    nivel_advertencia: NivelAdvertencia = Field(..., description="Nivel de severidad de la advertencia")

# --- Esquema para la Creación (Entrada) ---
# Hereda de la base. Lo mantenemos por consistencia para el CRUD.
class AdvertenciaCreate(AdvertenciaBase):
    pass

# --- Esquema para la Actualización (Entrada) ---
# Todos los campos son opcionales para permitir actualizaciones parciales.
class AdvertenciaUpdate(BaseModel):
    categoria: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    nivel_advertencia: Optional[NivelAdvertencia] = None

# --- Esquema Público (Salida) ---
# Este es el modelo que se devolverá al cliente. Incluye el 'id'.
class AdvertenciaPublic(AdvertenciaBase):
    id: int

    class Config:
        from_attributes = True