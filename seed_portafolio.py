from backend.core.config import settings
from backend.core.database import SessionLocal
from backend.core.security import hash_password
from backend.models.models import Usuario, Categoria, Obra, ImagenObra


def seed():
    db = SessionLocal()

    admin = db.query(Usuario).filter(Usuario.email == settings.ADMIN_EMAIL).first()
    if not admin:
        admin = Usuario(
            nombre="Administrador",
            email=settings.ADMIN_EMAIL,
            password_hash=hash_password(settings.ADMIN_PASSWORD),
            es_admin=True,
        )
        db.add(admin)
        db.flush()
        print(f"  + Admin creado: {settings.ADMIN_EMAIL}")
    else:
        print(f"  ~ Admin ya existe: {settings.ADMIN_EMAIL}")

    categorias_data = [
        {"id": 1, "nombre": "Barandas", "descripcion": "Barandas metálicas para interiores y exteriores"},
        {"id": 2, "nombre": "Rejas", "descripcion": "Rejas de seguridad para hogar y negocio"},
        {"id": 3, "nombre": "Puertas", "descripcion": "Puertas metálicas a medida"},
        {"id": 4, "nombre": "Estructuras", "descripcion": "Estructuras metálicas para construcción"},
        {"id": 5, "nombre": "Otros", "descripcion": "Diseños artísticos personalizados"},
    ]

    for cat_data in categorias_data:
        existe = db.query(Categoria).filter(Categoria.id == cat_data["id"]).first()
        if not existe:
            db.add(Categoria(**cat_data))
            print(f"  + Categoría: {cat_data['nombre']}")

    db.flush()

    obras_data = [
        {
            "categoria_id": 1,
            "titulo": "Baranda Moderna",
            "descripcion": "Baranda en acero con pasamanos de madera para interior residencial.",
            "ubicacion": "Armenia, Quindío",
            "imagen": "barandas1.jpg",
        },
        {
            "categoria_id": 2,
            "titulo": "Reja de Seguridad",
            "descripcion": "Reja para ventana con diseño de líneas rectas, acabado en pintura electrostática.",
            "ubicacion": "Armenia, Quindío",
            "imagen": "rejas1.jpg",
        },
        {
            "categoria_id": 3,
            "titulo": "Puerta Principal",
            "descripcion": "Puerta de acceso principal con detalles decorativos y cerradura de seguridad.",
            "ubicacion": "Armenia, Quindío",
            "imagen": "puertas1.jpg",
        },
        {
            "categoria_id": 3,
            "titulo": "Puerta de Garaje",
            "descripcion": "Puerta corrediza para garaje con estructura reforzada.",
            "ubicacion": "Armenia, Quindío",
            "imagen": "puertas2.jpg",
        },
        {
            "categoria_id": 4,
            "titulo": "Estructura Metálica",
            "descripcion": "Estructura para cubierta de área social con vigas de acero.",
            "ubicacion": "Armenia, Quindío",
            "imagen": "estructura1.jpg",
        },
    ]

    for obra_data in obras_data:
        imagen = obra_data.pop("imagen")
        obra = Obra(**obra_data)
        db.add(obra)
        db.flush()
        db.add(ImagenObra(obra_id=obra.id, url=f"/uploads/{imagen}", es_portada=True, orden=0))
        print(f"  + Obra: {obra_data['titulo']} → {imagen}")

    db.commit()
    db.close()


if __name__ == "__main__":
    print("Insertando datos de portafolio...")
    seed()
    print("¡Listo!")
