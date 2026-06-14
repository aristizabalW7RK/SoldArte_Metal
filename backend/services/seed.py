from backend.core.config import settings
from backend.core.database import SessionLocal
from backend.core.security import hash_password, verify_password
from backend.models.models import Usuario, Categoria, Obra, ImagenObra
from sqlalchemy import text
import os, shutil


def copiar_imagenes_seed():
    origen = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads_data")
    if not os.path.exists(origen):
        return
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    for archivo in ["barandas1.jpg", "estructura1.jpg", "puertas1.jpg", "puertas2.jpg", "rejas1.jpg"]:
        src = os.path.join(origen, archivo)
        dst = os.path.join(settings.UPLOAD_DIR, archivo)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"  + Imagen copiada: {archivo}")


def seed_admin():
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


def seed_portafolio():
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
        db.commit()
    except Exception as e:
        print(f"  ! Error al sembrar portafolio: {e}")
    finally:
        db.close()


def _reparar_secuencias():
    db = SessionLocal()
    try:
        if db.bind.dialect.name != "postgresql":
            return
        secuencias = [
            ("categoria_id_seq", "categoria"),
            ("obra_id_seq", "obra"),
            ("imagen_obra_id_seq", "imagen_obra"),
            ("producto_id_seq", "producto"),
            ("usuario_id_seq", "usuario"),
            ("cotizacion_id_seq", "cotizacion"),
        ]
        for seq, tabla in secuencias:
            db.execute(text(f"SELECT setval('{seq}', (SELECT COALESCE(MAX(id), 1) FROM {tabla}))"))
        db.commit()
        print("  ✓ Secuencias reparadas")
    except Exception as e:
        print(f"  ! Error reparando secuencias: {e}")
    finally:
        db.close()


def run_all():
    copiar_imagenes_seed()
    seed_admin()
    seed_portafolio()
    _reparar_secuencias()


def seed_if_empty():
    db = SessionLocal()
    try:
        if db.query(Obra).first() is not None:
            return
        print("DB vacía — ejecutando seed...")
        run_all()
    finally:
        db.close()


def ensure_admin():
    """Sincroniza el admin en cada startup: crea si no existe, o actualiza email/password si cambiaron."""
    db = SessionLocal()
    try:
        admin = db.query(Usuario).filter(Usuario.es_admin == True).first()
        pw_hash = hash_password(settings.ADMIN_PASSWORD)
        if not admin:
            db.add(Usuario(
                nombre="Administrador",
                email=settings.ADMIN_EMAIL,
                password_hash=pw_hash,
                es_admin=True,
            ))
            db.commit()
            print(f"  ✓ Admin creado: {settings.ADMIN_EMAIL}")
        else:
            cambios = False
            if admin.email != settings.ADMIN_EMAIL:
                admin.email = settings.ADMIN_EMAIL
                cambios = True
            if not verify_password(settings.ADMIN_PASSWORD, admin.password_hash):
                admin.password_hash = pw_hash
                admin.email = settings.ADMIN_EMAIL
                cambios = True
            if cambios:
                db.commit()
                print(f"  ✓ Admin sincronizado: {settings.ADMIN_EMAIL}")
    except Exception as e:
        print(f"  ! Error al sincronizar admin: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("Ejecutando seed...")
    run_all()
    print("¡Seed completado!")
