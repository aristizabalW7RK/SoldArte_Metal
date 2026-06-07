from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.core.database import engine, Base
from backend.api.routes import auth, portafolio, productos, cotizaciones
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Soldarte Metal API",
    description="Backend para la plataforma web de Soldarte Metal — herrería de obra y artística",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router, prefix="/api")
app.include_router(portafolio.router, prefix="/api")
app.include_router(productos.router, prefix="/api")
app.include_router(cotizaciones.router, prefix="/api")

@app.get("/")
def root():
    return {"mensaje": "Soldarte Metal API funcionando", "docs": "/docs"}
