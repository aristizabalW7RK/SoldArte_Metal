from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Obra, Categoria
from app.schemas.schemas import ObraCreate, ObraOut, CategoriaCreate, CategoriaOut

router = APIRouter(prefix="/portafolio", tags=["Portafolio"])

# Categorias
@router.get("/categorias", response_model=list[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

@router.post("/categorias", response_model=CategoriaOut, status_code=201)
def crear_categoria(datos: CategoriaCreate, db: Session = Depends(get_db)):
    categoria = Categoria(**datos.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

# Obras
@router.get("/obras", response_model=list[ObraOut])
def listar_obras(categoria_id: int | None = None, destacado: bool | None = None, db: Session = Depends(get_db)):
    query = db.query(Obra)
    if categoria_id:
        query = query.filter(Obra.categoria_id == categoria_id)
    if destacado is not None:
        query = query.filter(Obra.destacado == destacado)
    return query.order_by(Obra.created_at.desc()).all()

@router.get("/obras/{obra_id}", response_model=ObraOut)
def obtener_obra(obra_id: int, db: Session = Depends(get_db)):
    obra = db.query(Obra).filter(Obra.id == obra_id).first()
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    return obra

@router.post("/obras", response_model=ObraOut, status_code=201)
def crear_obra(datos: ObraCreate, db: Session = Depends(get_db)):
    obra = Obra(**datos.model_dump())
    db.add(obra)
    db.commit()
    db.refresh(obra)
    return obra

@router.put("/obras/{obra_id}", response_model=ObraOut)
def actualizar_obra(obra_id: int, datos: ObraCreate, db: Session = Depends(get_db)):
    obra = db.query(Obra).filter(Obra.id == obra_id).first()
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    for campo, valor in datos.model_dump().items():
        setattr(obra, campo, valor)
    db.commit()
    db.refresh(obra)
    return obra

@router.delete("/obras/{obra_id}", status_code=204)
def eliminar_obra(obra_id: int, db: Session = Depends(get_db)):
    obra = db.query(Obra).filter(Obra.id == obra_id).first()
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    db.delete(obra)
    db.commit()
