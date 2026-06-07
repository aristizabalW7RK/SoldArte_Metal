from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.models import Cotizacion, Favorito
from backend.schemas.schemas import CotizacionCreate, CotizacionOut, FavoritoOut

router = APIRouter(tags=["Cotizaciones y Favoritos"])

# Cotizaciones
@router.post("/cotizaciones", response_model=CotizacionOut, status_code=201)
def crear_cotizacion(datos: CotizacionCreate, db: Session = Depends(get_db)):
    cotizacion = Cotizacion(**datos.model_dump())
    db.add(cotizacion)
    db.commit()
    db.refresh(cotizacion)
    return cotizacion

@router.get("/cotizaciones", response_model=list[CotizacionOut])
def listar_cotizaciones(estado: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Cotizacion)
    if estado:
        query = query.filter(Cotizacion.estado == estado)
    return query.order_by(Cotizacion.created_at.desc()).all()

@router.patch("/cotizaciones/{cotizacion_id}/estado")
def cambiar_estado(cotizacion_id: int, estado: str, db: Session = Depends(get_db)):
    estados_validos = ["nueva", "en_revision", "respondida", "cerrada"]
    if estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Opciones: {estados_validos}")
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    cotizacion.estado = estado
    db.commit()
    return {"mensaje": "Estado actualizado"}

# Favoritos
@router.post("/usuarios/{usuario_id}/favoritos/{producto_id}", response_model=FavoritoOut, status_code=201)
def agregar_favorito(usuario_id: int, producto_id: int, db: Session = Depends(get_db)):
    existente = db.query(Favorito).filter_by(usuario_id=usuario_id, producto_id=producto_id).first()
    if existente:
        raise HTTPException(status_code=400, detail="El producto ya está en favoritos")
    favorito = Favorito(usuario_id=usuario_id, producto_id=producto_id)
    db.add(favorito)
    db.commit()
    db.refresh(favorito)
    return favorito

@router.get("/usuarios/{usuario_id}/favoritos", response_model=list[FavoritoOut])
def listar_favoritos(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(Favorito).filter(Favorito.usuario_id == usuario_id).all()

@router.delete("/usuarios/{usuario_id}/favoritos/{producto_id}", status_code=204)
def eliminar_favorito(usuario_id: int, producto_id: int, db: Session = Depends(get_db)):
    favorito = db.query(Favorito).filter_by(usuario_id=usuario_id, producto_id=producto_id).first()
    if not favorito:
        raise HTTPException(status_code=404, detail="Favorito no encontrado")
    db.delete(favorito)
    db.commit()
