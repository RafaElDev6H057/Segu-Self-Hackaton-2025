# routers/advertencia.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from models.advertencia import Advertencia
from schemas.advertencia import AdvertenciaCreate, AdvertenciaPublic, AdvertenciaUpdate
from core.db import get_session

# Creamos un nuevo router para las advertencias
router = APIRouter(
    prefix="/advertencias",
    tags=["Advertencias"]
)

@router.post("/", response_model=AdvertenciaPublic, status_code=status.HTTP_201_CREATED)
def create_advertencia(advertencia: AdvertenciaCreate, session: Session = Depends(get_session)):
    """
    Crea una nueva advertencia.
    """
    db_advertencia = Advertencia.model_validate(advertencia)
    session.add(db_advertencia)
    session.commit()
    session.refresh(db_advertencia)
    return db_advertencia

@router.get("/", response_model=List[AdvertenciaPublic])
def get_all_advertencias(session: Session = Depends(get_session)):
    """
    Obtiene una lista de todas las advertencias.
    """
    advertencias = session.exec(select(Advertencia)).all()
    return advertencias

@router.get("/{advertencia_id}", response_model=AdvertenciaPublic)
def get_advertencia_by_id(advertencia_id: int, session: Session = Depends(get_session)):
    """
    Obtiene una advertencia específica por su ID.
    """
    db_advertencia = session.get(Advertencia, advertencia_id)
    if not db_advertencia:
        raise HTTPException(status_code=404, detail="Advertencia no encontrada")
    return db_advertencia

@router.put("/{advertencia_id}", response_model=AdvertenciaPublic)
def update_advertencia(advertencia_id: int, advertencia_update: AdvertenciaUpdate, session: Session = Depends(get_session)):
    """
    Actualiza una advertencia por su ID.
    """
    db_advertencia = session.get(Advertencia, advertencia_id)
    if not db_advertencia:
        raise HTTPException(status_code=404, detail="Advertencia no encontrada")

    update_data = advertencia_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_advertencia, key, value)
        
    session.add(db_advertencia)
    session.commit()
    session.refresh(db_advertencia)
    
    return db_advertencia

@router.delete("/{advertencia_id}", status_code=status.HTTP_200_OK)
def delete_advertencia(advertencia_id: int, session: Session = Depends(get_session)):
    """
    Elimina una advertencia por su ID.
    """
    db_advertencia = session.get(Advertencia, advertencia_id)
    if not db_advertencia:
        raise HTTPException(status_code=404, detail="Advertencia no encontrada")
        
    session.delete(db_advertencia)
    session.commit()
    
    return {"message": "Advertencia eliminada exitosamente"}