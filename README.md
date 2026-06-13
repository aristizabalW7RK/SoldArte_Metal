# SoldArte Metal

Plataforma web para **SoldArte Metal** — empresa de herrería de obra y artística ubicada en Armenia, Quindío, Colombia.

- **Frontend**: Angular 22 (standalone components, Signals, Vitest)
- **Backend**: Python / FastAPI + SQLAlchemy + PostgreSQL
- **Autenticación**: JWT + bcrypt
- **Deploy**: Railway (API) + Vercel (frontend)

---

## Stack

| Capa | Tecnología |
|------|------------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2 |
| Base de datos | PostgreSQL (Docker Compose local / Railway en prod) |
| Migraciones | Alembic (autogenerate) |
| Autenticación | JWT (HS256) + bcrypt |
| Frontend | Angular 22, standalone components, Signals |
| Testing | pytest (backend), Vitest (frontend) |
| Deploy | Railway (backend), Vercel (frontend), nixpacks |

---

## Requisitos

- Python 3.12+
- Node.js 22+
- Docker y Docker Compose (opcional, para PostgreSQL local)

---

## Setup rápido (backend)

```bash
# 1. Clonar
git clone <repo>
cd soldarte-metal

# 2. Entorno virtual
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Variables de entorno
cp .env.example .env
# Editar .env con los valores correspondientes

# 4. Base de datos (PostgreSQL)
docker compose up -d

# 5. Migraciones
python3 -m alembic upgrade head

# 6. Seed inicial (opcional)
python3 -m backend.services.seed

# 7. Iniciar servidor
uvicorn main:app --reload
```

La API queda en `http://localhost:8000`.  
Documentación interactiva: `http://localhost:8000/docs`

---

## Setup frontend

```bash
cd soldarte-frontend
npm install
npm start
```

Desarrolla en `http://localhost:4200`.

---

## Seed de datos

El seed crea un usuario administrador, 5 categorías y 5 obras de ejemplo con imágenes.

```bash
python3 -m backend.services.seed
```

Variables que controla el seed (desde `.env`):

| Variable | Descripción |
|----------|-------------|
| `ADMIN_EMAIL` | Email del administrador |
| `ADMIN_PASSWORD` | Contraseña del administrador |

> El seed se ejecuta **una sola vez, de forma explícita** (no en cada startup).

---

## Migraciones (Alembic)

El proyecto usa Alembic para control de cambios en la base de datos.

```bash
# Crear una nueva migración tras modificar modelos
python3 -m alembic revision --autogenerate -m "descripcion"

# Aplicar migraciones pendientes
python3 -m alembic upgrade head

# Ver estado
python3 -m alembic current
```

---

## Tests

```bash
# Backend (64 tests)
python3 -m pytest backend/tests/ -v

# Frontend (10 tests)
cd soldarte-frontend && npm test
```

---

## Estructura del proyecto

```
soldarte-metal/
├── main.py                       # Punto de entrada de la API
├── docker-compose.yml            # PostgreSQL local
├── requirements.txt              # Dependencias Python
├── nixpacks.toml                 # Config de deploy Railway
├── alembic/                      # Migraciones
│   ├── env.py
│   └── versions/
├── backend/
│   ├── core/
│   │   ├── config.py             # Settings con pydantic-settings
│   │   ├── database.py           # Engine, SessionLocal, get_db
│   │   ├── security.py           # JWT + bcrypt
│   │   └── deps.py               # Dependencias (get_current_user, get_current_admin)
│   ├── models/
│   │   └── models.py             # SQLAlchemy: Usuario, Categoria, Obra, ImagenObra, Producto, Cotizacion, Favorito
│   ├── schemas/
│   │   └── schemas.py            # Pydantic v2: request/response
│   ├── services/
│   │   ├── seed.py               # Seed de datos
│   │   └── file_service.py       # Subida de imágenes
│   ├── api/routes/
│   │   ├── auth.py               # POST /registro, /login, GET /me
│   │   ├── portafolio.py         # CRUD obras + categorías
│   │   ├── productos.py          # CRUD productos
│   │   └── cotizaciones.py       # Cotizaciones + favoritos
│   └── tests/
│       ├── conftest.py           # Fixtures (SQLite in-memory)
│       ├── test_auth.py
│       ├── test_cotizaciones.py
│       ├── test_portafolio.py
│       ├── test_productos.py
│       ├── test_schemas.py
│       └── test_security.py
├── soldarte-frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/       # Navbar
│   │   │   ├── guards/           # auth.guard.ts, admin.guard.ts
│   │   │   ├── pages/            # Inicio, Portafolio, Productos, Cotizacion, Login, Registro, Perfil, Admin
│   │   │   └── services/         # Api, Auth, Productos, Portafolio, Cotizacion, Tema
│   │   ├── environments/         # environment.ts / environment.prod.ts
│   │   └── styles.css            # Tema oscuro/claro con custom properties
│   ├── angular.json
│   └── package.json
└── uploads_data/                 # Imágenes de ejemplo para el seed
```

---

## API — Endpoints principales

### Autenticación
| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/api/auth/registro` | — | Registrar usuario |
| POST | `/api/auth/login` | — | Login → JWT |
| GET | `/api/auth/me` | Bearer | Perfil del usuario |

### Portafolio
| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/api/portafolio/categorias` | — | Listar categorías |
| POST | `/api/portafolio/categorias` | Admin | Crear categoría |
| GET | `/api/portafolio/obras` | — | Listar obras (`?categoria_id=&destacado=`) |
| POST | `/api/portafolio/obras` | Admin | Crear obra |
| PUT | `/api/portafolio/obras/{id}` | Admin | Actualizar obra |
| DELETE | `/api/portafolio/obras/{id}` | Admin | Eliminar obra |
| POST | `/api/portafolio/obras/{id}/imagenes` | Admin | Subir imagen de obra |

### Productos
| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/api/productos` | — | Listar productos (`?solo_disponibles=`) |
| POST | `/api/productos` | Admin | Crear producto |
| PUT | `/api/productos/{id}` | Admin | Actualizar producto |
| DELETE | `/api/productos/{id}` | Admin | Eliminar producto |
| POST | `/api/productos/{id}/imagen` | Admin | Subir imagen de producto |

### Cotizaciones
| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/api/cotizaciones` | — | Crear cotización |
| GET | `/api/cotizaciones` | Admin | Listar (`?estado=`) |
| PATCH | `/api/cotizaciones/{id}/estado` | Admin | Cambiar estado |

### Favoritos
| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/api/usuarios/{id}/favoritos/{id}` | Bearer | Agregar favorito |
| GET | `/api/usuarios/{id}/favoritos` | Bearer | Listar favoritos |
| DELETE | `/api/usuarios/{id}/favoritos/{id}` | Bearer | Eliminar favorito |

---

## Variables de entorno (`.env`)

| Variable | Default | Descripción |
|----------|---------|-------------|
| `DATABASE_URL` | — | Conexión PostgreSQL |
| `SECRET_KEY` | — | Clave para firmar JWT |
| `ALGORITHM` | `HS256` | Algoritmo JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Expiración del token |
| `UPLOAD_DIR` | `uploads` | Directorio de imágenes |
| `ADMIN_EMAIL` | — | Email del admin para seed |
| `ADMIN_PASSWORD` | — | Contraseña del admin para seed |

---

## Deploy

### Backend — Railway

El archivo `nixpacks.toml` define el comando de inicio:

```toml
start = "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT"
```

Agregar `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `SECRET_KEY` y `DATABASE_URL` desde el dashboard de Railway.

### Frontend — Vercel

El `vercel.json` ya está configurado con SPA fallback y output en `dist/soldarte-frontend/browser`.

Las variables de entorno se configuran en Vercel:
- `API_URL` → `https://soldartemetal-production.up.railway.app`
