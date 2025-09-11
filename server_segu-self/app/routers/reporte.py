# routers/reporte.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from models.reporte import Reporte
from models.user import User  # Importamos el modelo User
from schemas.reporte import ReporteCreate, ReportePublic, ReporteUpdate
from core.db import get_session

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

@router.post("/", response_model=ReportePublic, status_code=status.HTTP_201_CREATED)
def create_reporte(reporte: ReporteCreate, session: Session = Depends(get_session)):
    """
    Crea un nuevo reporte y lo asocia a un usuario por su email.
    """
    # 1. Buscar al usuario por el email proporcionado.
    db_user = session.exec(select(User).where(User.email == reporte.usuario_email)).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un usuario con el email {reporte.usuario_email}"
        )
    
    # 2. Crear el reporte asociando el ID del usuario encontrado.
    # Usamos model_dump para excluir el campo extra 'usuario_email' del schema.
    report_data = reporte.model_dump(exclude={"usuario_email"})
    if db_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario encontrado no tiene un ID válido"
        )
    db_reporte = Reporte(**report_data, usuario_id=db_user.id)
    
    session.add(db_reporte)
    session.commit()
    session.refresh(db_reporte)
    return db_reporte

# --- El resto de los endpoints (GET, PUT, DELETE) funcionan sin cambios ---
# SQLModel carga automáticamente la relación 'usuario' cuando se accede a ella,
# por lo que el `response_model=ReportePublic` funcionará correctamente.

@router.get("/", response_model=List[ReportePublic])
def get_all_reportes(session: Session = Depends(get_session)):
    reportes = session.exec(select(Reporte)).all()
    return reportes

@router.get("/{reporte_id}", response_model=ReportePublic)
def get_reporte_by_id(reporte_id: int, session: Session = Depends(get_session)):
    db_reporte = session.get(Reporte, reporte_id)
    if not db_reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return db_reporte

# ... (PUT y DELETE sin cambios) ...
@router.put("/{reporte_id}", response_model=ReportePublic)
def update_reporte(reporte_id: int, reporte_update: ReporteUpdate, session: Session = Depends(get_session)):
    db_reporte = session.get(Reporte, reporte_id)
    if not db_reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    update_data = reporte_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_reporte, key, value)
    session.add(db_reporte)
    session.commit()
    session.refresh(db_reporte)
    return db_reporte

@router.delete("/{reporte_id}", status_code=status.HTTP_200_OK)
def delete_reporte(reporte_id: int, session: Session = Depends(get_session)):
    db_reporte = session.get(Reporte, reporte_id)
    if not db_reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    session.delete(db_reporte)
    session.commit()
    return {"message": "Reporte eliminado exitosamente"}