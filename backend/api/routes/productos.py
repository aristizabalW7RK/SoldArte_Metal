from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.deps import get_current_admin
from backend.models.models import Producto, Usuario
from backend.schemas.schemas import ProductoCreate, ProductoOut
from backend.services.file_service import save_upload

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("", response_model=list[ProductoOut])
def listar_productos(solo_disponibles: bool = True, db: Session = Depends(get_db)):
    query = db.query(Producto)
    if solo_disponibles:
        query = query.filter(Producto.disponible == True)
    return query.order_by(Producto.nombre).all()

@router.get("/{producto_id}", response_model=ProductoOut)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("", response_model=ProductoOut, status_code=201)
def crear_producto(datos: ProductoCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_admin)):
    producto = Producto(**datos.model_dump())
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto

@router.put("/{producto_id}", response_model=ProductoOut)
def actualizar_producto(producto_id: int, datos: ProductoCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_admin)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for campo, valor in datos.model_dump().items():
        setattr(producto, campo, valor)
    db.commit()
    db.refresh(producto)
    return producto

@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_admin)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()

@router.post("/{producto_id}/imagen", response_model=ProductoOut)
def subir_imagen_producto(producto_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_admin)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.imagen_url = save_upload(file)
    db.commit()
    db.refresh(producto)
    return producto
