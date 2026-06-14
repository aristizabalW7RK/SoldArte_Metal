from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.deps import get_current_admin
from backend.models.models import Obra, Categoria, ImagenObra, Usuario
from backend.schemas.schemas import ObraCreate, ObraOut, CategoriaCreate, CategoriaOut, ImagenObraOut
from backend.services.file_service import save_upload

router = APIRouter(prefix="/portafolio", tags=["Portafolio"])

# Categorias
@router.get("/categorias", response_model=list[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

@router.post("/categorias", response_model=CategoriaOut, status_code=201)
def crear_categoria(datos: CategoriaCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_admin)):
    categoria = Categoria(**datos.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

@router.put("/categorias/{categoria_id}", response_model=CategoriaOut)
def actualizar_categoria(categoria_id: int, datos: CategoriaCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_admin)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    for campo, valor in datos.model_dump().items():
        setattr(categoria, campo, valor)
    db.commit()
    db.refresh(categoria)
    return categoria

@router.delete("/categorias/{categoria_id}", status_code=204)
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_admin)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if db.query(Obra).filter(Obra.categoria_id == categoria_id).first():
        raise HTTPException(status_code=400, detail="No se puede eliminar una categoría con obras asociadas")
    db.delete(categoria)
    db.commit()

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
def crear_obra(datos: ObraCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_admin)):
    obra = Obra(**datos.model_dump())
    db.add(obra)
    db.commit()
    db.refresh(obra)
    return obra

@router.put("/obras/{obra_id}", response_model=ObraOut)
def actualizar_obra(obra_id: int, datos: ObraCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_admin)):
    obra = db.query(Obra).filter(Obra.id == obra_id).first()
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    for campo, valor in datos.model_dump().items():
        setattr(obra, campo, valor)
    db.commit()
    db.refresh(obra)
    return obra

@router.delete("/obras/{obra_id}", status_code=204)
def eliminar_obra(obra_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_admin)):
    obra = db.query(Obra).filter(Obra.id == obra_id).first()
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    db.delete(obra)
    db.commit()

@router.post("/obras/{obra_id}/imagenes", response_model=ImagenObraOut, status_code=201)
def subir_imagen_obra(
    obra_id: int,
    file: UploadFile = File(...),
    es_portada: bool = False,
    orden: int = 0,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_admin),
):
    obra = db.query(Obra).filter(Obra.id == obra_id).first()
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    url = save_upload(file)
    if es_portada:
        db.query(ImagenObra).filter(ImagenObra.obra_id == obra_id, ImagenObra.es_portada == True).update({"es_portada": False})
    imagen = ImagenObra(obra_id=obra_id, url=url, es_portada=es_portada, orden=orden)
    db.add(imagen)
    db.commit()
    db.refresh(imagen)
    return imagen
