from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from models.user import User
from schemas.user import UserCreate, UserPublic, UserLogin, UserUpdate 
from core.db import get_session
from core.security import hash_password, verify_password

# Creamos un nuevo router con el prefijo y tags en español
router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.post("/registrar", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Registra un nuevo usuario en la base de datos.
    """
    # Verificamos si ya existe un usuario con el mismo email (único campo que no debe repetirse)
    db_user_by_email = session.exec(select(User).where(User.email == user_create.email)).first()

    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo electrónico ya está registrado."
        )

    # Hasheamos la contraseña antes de guardarla
    hashed_pass = hash_password(user_create.password)
    
    # Creamos la instancia del modelo User usando model_validate
    user_data = user_create.model_dump(exclude={"password"})
    db_user = User(**user_data, hashed_password=hashed_pass)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@router.post("/iniciar_sesion")
def login_for_user(form_data: UserLogin, session: Session = Depends(get_session)):
    """
    Inicia sesión con correo y contraseña.
    """
    user = session.exec(select(User).where(User.email == form_data.email)).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"message": "Inicio de sesión exitoso", "status": 201}

@router.get("/", response_model=List[UserPublic])
def get_all_users(session: Session = Depends(get_session)):
    """
    Recupera una lista de todos los usuarios.
    """
    users = session.exec(select(User)).all()
    return users

@router.get("/{usuario_id}", response_model=UserPublic)
def get_user_by_id(usuario_id: int, session: Session = Depends(get_session)):
    """
    Recupera un usuario por su ID.
    """
    db_user = session.get(User, usuario_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@router.put("/{usuario_id}", response_model=UserPublic)
def update_user(usuario_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    """
    Actualiza la información de un usuario por su ID.
    """
    db_user = session.get(User, usuario_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user

@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
def delete_user(usuario_id: int, session: Session = Depends(get_session)):
    """
    Elimina un usuario de la base de datos por su ID.
    """
    db_user = session.get(User, usuario_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    session.delete(db_user)
    session.commit()
    
    return {"message": "Usuario eliminado exitosamente"}
