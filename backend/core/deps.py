from fastapi import HTTPException, Depends, Request
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.security import decode_token
from backend.models.models import Usuario


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> Usuario:
    auth = request.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
        token = auth.removeprefix("Bearer ")
    else:
        token = request.cookies.get("soldarte_token")
    if not token:
        raise HTTPException(status_code=401, detail="No autenticado")
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    usuario = db.query(Usuario).filter(Usuario.id == int(payload["sub"])).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return usuario


def get_current_admin(
    usuario: Usuario = Depends(get_current_user),
) -> Usuario:
    if not usuario.es_admin:
        raise HTTPException(status_code=403, detail="Se requieren permisos de administrador")
    return usuario
