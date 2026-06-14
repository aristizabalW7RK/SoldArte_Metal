import logging

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.deps import get_current_user
from backend.core.security import hash_password, verify_password, create_access_token
from backend.core.config import settings
from backend.models.models import Usuario
from backend.schemas.schemas import UsuarioCreate, UsuarioOut, LoginSchema

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Autenticación"])


def _set_token_cookie(response: Response, token: str):
    response.set_cookie(
        key="soldarte_token",
        value=token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="none" if not settings.DEBUG else "lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )


@router.post("/registro", response_model=UsuarioOut, status_code=201)
def registrar_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    from sqlalchemy import func
    email = datos.email.lower().strip()
    if db.query(Usuario).filter(func.lower(Usuario.email) == email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    usuario = Usuario(
        nombre=datos.nombre,
        telefono=datos.telefono,
        email=email,
        password_hash=hash_password(datos.password),
        fecha_nacimiento=datos.fecha_nacimiento,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=UsuarioOut)
def login(datos: LoginSchema, response: Response, db: Session = Depends(get_db)):
    from sqlalchemy import func
    usuario = db.query(Usuario).filter(func.lower(Usuario.email) == func.lower(datos.email)).first()
    if not usuario:
        logger.warning(f"Login fallido: email no registrado — {datos.email}")
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    if not verify_password(datos.password, usuario.password_hash):
        logger.warning(f"Login fallido: contraseña incorrecta — {datos.email}")
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    logger.info(f"Login exitoso: {datos.email}")
    token = create_access_token({
        "sub": str(usuario.id),
        "nombre": usuario.nombre,
        "email": usuario.email,
        "es_admin": usuario.es_admin,
    })
    _set_token_cookie(response, token)
    return usuario


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("soldarte_token", path="/")
    return {"mensaje": "Sesión cerrada"}


@router.get("/me", response_model=UsuarioOut)
def obtener_perfil(usuario: Usuario = Depends(get_current_user)):
    return usuario
