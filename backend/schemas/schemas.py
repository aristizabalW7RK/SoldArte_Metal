import re
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
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

    @field_validator("password")
    @classmethod
    def password_segura(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe contener al menos una mayúscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("La contraseña debe contener al menos una minúscula")
        if not re.search(r"\d", v):
            raise ValueError("La contraseña debe contener al menos un número")
        if not re.search(r"[!@#$%^&*()_\-+=\[\]{}|;:'\",.<>?/\\~`]", v):
            raise ValueError("La contraseña debe contener al menos un símbolo especial")
        return v

    @field_validator("telefono")
    @classmethod
    def telefono_colombiano(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(r"^(\+57)?3\d{9}$", v):
            raise ValueError("El teléfono debe ser un número celular colombiano válido (ej: 3001234567 o +573001234567)")
        return v

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: Optional[str]
    es_admin: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

# --- Imagen Obra ---
class ImagenObraOut(BaseModel):
    id: int
    url: str
    es_portada: bool
    orden: int
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

# --- Favorito ---
class FavoritoOut(BaseModel):
    id: int
    producto: ProductoOut
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
