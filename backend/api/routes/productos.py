from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.deps import get_current_admin
from backend.models.models import Producto, ImagenProducto, Usuario
from backend.schemas.schemas import ProductoCreate, ProductoOut, ImagenProductoOut
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

@router.post("/{producto_id}/imagenes", response_model=ImagenProductoOut, status_code=201)
def subir_imagen_producto(
    producto_id: int,
    file: UploadFile = File(...),
    es_portada: bool = False,
    orden: int = 0,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_admin),
):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    url = save_upload(file)
    if es_portada:
        db.query(ImagenProducto).filter(
            ImagenProducto.producto_id == producto_id, ImagenProducto.es_portada == True
        ).update({"es_portada": False})
    imagen = ImagenProducto(producto_id=producto_id, url=url, es_portada=es_portada, orden=orden)
    db.add(imagen)
    producto.imagen_url = url
    db.commit()
    db.refresh(imagen)
    return imagen

@router.delete("/{producto_id}/imagenes/{imagen_id}", status_code=204)
def eliminar_imagen_producto(
    producto_id: int,
    imagen_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_admin),
):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    imagen = db.query(ImagenProducto).filter(
        ImagenProducto.id == imagen_id, ImagenProducto.producto_id == producto_id
    ).first()
    if not imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    db.delete(imagen)
    restantes = db.query(ImagenProducto).filter(ImagenProducto.producto_id == producto_id).count()
    if restantes > 0:
        producto.imagen_url = db.query(ImagenProducto).filter(
            ImagenProducto.producto_id == producto_id
        ).order_by(ImagenProducto.orden, ImagenProducto.id).first().url
    else:
        producto.imagen_url = None
    db.commit()
