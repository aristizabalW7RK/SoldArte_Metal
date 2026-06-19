from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20))
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    es_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    cotizaciones = relationship("Cotizacion", back_populates="usuario")
    favoritos = relationship("Favorito", back_populates="usuario")


class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)

    obras = relationship("Obra", back_populates="categoria")


class Obra(Base):
    __tablename__ = "obra"
    id = Column(Integer, primary_key=True, index=True)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    ubicacion = Column(String(200), nullable=True)
    fecha_realizacion = Column(Date, nullable=True)
    destacado = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    categoria = relationship("Categoria", back_populates="obras")
    imagenes = relationship("ImagenObra", back_populates="obra", cascade="all, delete-orphan")


class ImagenObra(Base):
    __tablename__ = "imagen_obra"
    id = Column(Integer, primary_key=True, index=True)
    obra_id = Column(Integer, ForeignKey("obra.id"), nullable=False)
    url = Column(String(500), nullable=False)
    es_portada = Column(Boolean, default=False)
    orden = Column(Integer, default=0)

    obra = relationship("Obra", back_populates="imagenes")


class Producto(Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    referencia = Column(String(100), nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0)
    disponible = Column(Boolean, default=True)
    imagen_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    favoritos = relationship("Favorito", back_populates="producto")
    imagenes = relationship("ImagenProducto", back_populates="producto", cascade="all, delete-orphan")


class ImagenProducto(Base):
    __tablename__ = "imagen_producto"
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("producto.id"), nullable=False)
    url = Column(String(500), nullable=False)
    es_portada = Column(Boolean, default=False)
    orden = Column(Integer, default=0)

    producto = relationship("Producto", back_populates="imagenes")


class Cotizacion(Base):
    __tablename__ = "cotizacion"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=True)
    nombre_cliente = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    tipo_trabajo = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    direccion = Column(String(300), nullable=True)
    estado = Column(String(50), default="nueva")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", back_populates="cotizaciones")


class Favorito(Base):
    __tablename__ = "favorito"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("producto.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", back_populates="favoritos")
    producto = relationship("Producto", back_populates="favoritos")
