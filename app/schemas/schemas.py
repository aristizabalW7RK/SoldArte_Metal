from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

# --- Usuario ---
class UsuarioCreate(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    email: EmailStr
    password: str
    fecha_nacimiento: Optional[date] = None

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: Optional[str]
    created_at: datetime
    class Config: from_attributes = True

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Categoria ---
class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaOut(CategoriaCreate):
    id: int
    class Config: from_attributes = True

# --- Imagen Obra ---
class ImagenObraOut(BaseModel):
    id: int
    url: str
    es_portada: bool
    orden: int
    class Config: from_attributes = True

# --- Obra ---
class ObraCreate(BaseModel):
    categoria_id: int
    titulo: str
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = None
    fecha_realizacion: Optional[date] = None
    destacado: bool = False

class ObraOut(ObraCreate):
    id: int
    created_at: datetime
    imagenes: list[ImagenObraOut] = []
    categoria: CategoriaOut
    class Config: from_attributes = True

# --- Producto ---
class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    referencia: Optional[str] = None
    precio: Decimal
    stock: int = 0
    disponible: bool = True

class ProductoOut(ProductoCreate):
    id: int
    imagen_url: Optional[str]
    created_at: datetime
    class Config: from_attributes = True

# --- Cotizacion ---
class CotizacionCreate(BaseModel):
    nombre_cliente: str
    telefono: str
    email: EmailStr
    tipo_trabajo: str
    descripcion: str
    direccion: Optional[str] = None
    usuario_id: Optional[int] = None

class CotizacionOut(CotizacionCreate):
    id: int
    estado: str
    created_at: datetime
    class Config: from_attributes = True

# --- Favorito ---
class FavoritoOut(BaseModel):
    id: int
    producto: ProductoOut
    created_at: datetime
    class Config: from_attributes = True
