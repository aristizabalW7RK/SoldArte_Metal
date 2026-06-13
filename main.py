from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.core.database import engine, Base
from backend.core.config import settings
from backend.api.routes import auth, portafolio, productos, cotizaciones
import os

Base.metadata.create_all(bind=engine)

from backend.core.database import SessionLocal
from backend.core.security import hash_password, verify_password
from backend.models.models import Usuario, Categoria, Obra, ImagenObra

def _seed_admin():
    db = SessionLocal()
    try:
        admin = db.query(Usuario).filter(Usuario.email == settings.ADMIN_EMAIL).first()
        if not admin:
            db.add(Usuario(
                nombre="Administrador",
                email=settings.ADMIN_EMAIL,
                password_hash=hash_password(settings.ADMIN_PASSWORD),
                es_admin=True,
            ))
            db.commit()
            print(f"  ✓ Admin creado: {settings.ADMIN_EMAIL}")
        elif not verify_password(settings.ADMIN_PASSWORD, admin.password_hash):
            admin.password_hash = hash_password(settings.ADMIN_PASSWORD)
            db.commit()
            print(f"  ✓ Contraseña de admin actualizada")
    except Exception as e:
        print(f"  ! No se pudo crear admin: {e}")
    finally:
        db.close()


def _seed_portafolio():
    db = SessionLocal()
    try:
        categorias_data = [
            {"id": 1, "nombre": "Barandas", "descripcion": "Barandas metálicas para interiores y exteriores"},
            {"id": 2, "nombre": "Rejas", "descripcion": "Rejas de seguridad para hogar y negocio"},
            {"id": 3, "nombre": "Puertas", "descripcion": "Puertas metálicas a medida"},
            {"id": 4, "nombre": "Estructuras", "descripcion": "Estructuras metálicas para construcción"},
            {"id": 5, "nombre": "Otros", "descripcion": "Diseños artísticos personalizados"},
        ]
        for cat in categorias_data:
            if not db.query(Categoria).filter(Categoria.id == cat["id"]).first():
                db.add(Categoria(**cat))
                print(f"  + Categoría: {cat['nombre']}")

        obras_data = [
            {"categoria_id": 1, "titulo": "Baranda Moderna", "descripcion": "Baranda en acero con pasamanos de madera para interior residencial.", "ubicacion": "Armenia, Quindío", "imagen": "barandas1.jpg"},
            {"categoria_id": 2, "titulo": "Reja de Seguridad", "descripcion": "Reja para ventana con diseño de líneas rectas, acabado en pintura electrostática.", "ubicacion": "Armenia, Quindío", "imagen": "rejas1.jpg"},
            {"categoria_id": 3, "titulo": "Puerta Principal", "descripcion": "Puerta de acceso principal con detalles decorativos y cerradura de seguridad.", "ubicacion": "Armenia, Quindío", "imagen": "puertas1.jpg"},
            {"categoria_id": 3, "titulo": "Puerta de Garaje", "descripcion": "Puerta corrediza para garaje con estructura reforzada.", "ubicacion": "Armenia, Quindío", "imagen": "puertas2.jpg"},
            {"categoria_id": 4, "titulo": "Estructura Metálica", "descripcion": "Estructura para cubierta de área social con vigas de acero.", "ubicacion": "Armenia, Quindío", "imagen": "estructura1.jpg"},
        ]
        for obra_data in obras_data:
            if db.query(Obra).filter(Obra.titulo == obra_data["titulo"]).first():
                continue
            imagen = obra_data.pop("imagen")
            obra = Obra(**obra_data)
            db.add(obra)
            db.flush()
            db.add(ImagenObra(obra_id=obra.id, url=f"/uploads/{imagen}", es_portada=True, orden=0))
            print(f"  + Obra: {obra_data['titulo']}")
    except Exception as e:
        print(f"  ! Error al sembrar portafolio: {e}")
    finally:
        db.close()


_seed_admin()
_seed_portafolio()

app = FastAPI(
    title="Soldarte Metal API",
    description="Backend para la plataforma web de Soldarte Metal — herrería de obra y artística",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "https://soldartemetal-production.up.railway.app",
        "https://soldarte-metal.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth.router, prefix="/api")
app.include_router(portafolio.router, prefix="/api")
app.include_router(productos.router, prefix="/api")
app.include_router(cotizaciones.router, prefix="/api")

@app.get("/")
def root():
    return {"mensaje": "Soldarte Metal API funcionando", "docs": "/docs"}
