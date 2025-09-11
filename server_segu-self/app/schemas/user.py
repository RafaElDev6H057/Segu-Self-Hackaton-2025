from pydantic import BaseModel, EmailStr, Field, PositiveInt
from typing import Optional, List
from datetime import date, time

# --- Esquema Base con la nueva estructura ---
class UserBase(BaseModel):
    """
    Esquema base para el usuario con los campos actualizados.
    """
    nombre: str = Field(..., max_length=50, description="Nombre(s) del usuario")
    apellido_paterno: str = Field(..., max_length=50, description="Apellido paterno del usuario")
    apellido_materno: Optional[str] = Field(None, max_length=50, description="Apellido materno del usuario (opcional)")
    edad: PositiveInt = Field(..., description="Edad del usuario, debe ser un número positivo")
    direccion: str = Field(..., max_length=255, description="Dirección de residencia del usuario")
    email: EmailStr
    telefono: str

# --- Esquema para la Creación de un Usuario ---
class UserCreate(UserBase):
    """
    Esquema para crear un nuevo usuario. Hereda de UserBase y añade la contraseña.
    """
    password: str = Field(..., min_length=8, description="La contraseña debe tener al menos 8 caracteres")

# --- Esquema para la Actualización de un Usuario ---
class UserUpdate(BaseModel):
    """
    Esquema para actualizar un usuario. Todos los campos son opcionales.
    """
    nombre: Optional[str] = Field(None, max_length=50)
    apellido_paterno: Optional[str] = Field(None, max_length=50)
    apellido_materno: Optional[str] = Field(None, max_length=50)
    edad: Optional[PositiveInt] = None
    direccion: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, min_length=7, max_length=15)

# --- Esquema para el Inicio de Sesión (SIN CAMBIOS) ---
class UserLogin(BaseModel):
    """
    Esquema para el login de usuario, requiere email y contraseña.
    """
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., description="Contraseña del usuario")

# --- Esquema Público para mostrar información (SIN CONTRASEÑA) ---
class UserPublic(UserBase):
    """
    Esquema para mostrar la información pública del usuario.
    """
    id: int

    class Config:
        """
        Configuración para permitir que Pydantic trabaje con modelos de ORM (como SQLModel).
        """
        from_attributes = True

class ReporteInUserPublic(BaseModel):
    id: int
    fecha: date
    hora: time
    tipo_evento: str
    descripcion: str
    
    class Config:
        from_attributes = True

# Un nuevo esquema público de Usuario que SÍ incluye sus reportes.
class UserPublicWithReports(UserPublic):
    reportes: List[ReporteInUserPublic] = []