from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.core.database import engine, Base
from backend.core.config import settings
from backend.api.routes import auth, portafolio, productos, cotizaciones
import os

Base.metadata.create_all(bind=engine)

from backend.core.database import SessionLocal
from backend.core.security import hash_password
from backend.models.models import Usuario

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
    except Exception as e:
        print(f"  ! No se pudo crear admin: {e}")
    finally:
        db.close()

_seed_admin()

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
        "https://soldarte.vercel.app",
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
