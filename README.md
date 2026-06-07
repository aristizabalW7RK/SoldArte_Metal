# Soldarte Metal — Backend API

Backend construido con FastAPI + PostgreSQL + Docker.

## Requisitos
- Docker y Docker Compose instalados
- Python 3.12 (solo si corres sin Docker)

## Arrancar el proyecto

### 1. Clonar y configurar variables de entorno
```bash
cp .env.example .env
# Edita .env con tus valores reales
```

### 2. Levantar con Docker
```bash
docker-compose up --build
```

La API queda disponible en: http://localhost:8000  
Documentación interactiva (Swagger): http://localhost:8000/docs

## Estructura del proyecto
```
soldarte-backend/
├── main.py              # Punto de entrada
├── backend/
│   ├── core/
│   │   ├── config.py        # Variables de entorno
│   │   ├── database.py      # Conexión PostgreSQL
│   │   └── security.py      # JWT y bcrypt
│   ├── models/
│   │   └── models.py        # Tablas SQLAlchemy
│   ├── schemas/
│   │   └── schemas.py       # Validación Pydantic
│   └── api/routes/
│       ├── auth.py          # Registro y login
│       ├── portafolio.py    # Obras y categorías
│       ├── productos.py     # Catálogo de productos
│       └── cotizaciones.py  # Cotizaciones y favoritos
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /api/auth/registro | Registrar usuario |
| POST | /api/auth/login | Login → retorna JWT |
| GET | /api/portafolio/obras | Listar obras del portafolio |
| GET | /api/portafolio/categorias | Listar categorías |
| GET | /api/productos | Listar productos disponibles |
| POST | /api/cotizaciones | Crear cotización |
| POST | /api/usuarios/{id}/favoritos/{id} | Agregar favorito |

## Cors
Por defecto permite peticiones desde `http://localhost:4200` (Angular en desarrollo).
Para producción, actualiza `allow_origins` en `backend/main.py`.
