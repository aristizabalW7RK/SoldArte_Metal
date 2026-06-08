import pytest
from pydantic import ValidationError
from decimal import Decimal
from datetime import date

from backend.schemas.schemas import (
    UsuarioCreate,
    LoginSchema,
    CategoriaCreate,
    ObraCreate,
    ProductoCreate,
    CotizacionCreate,
)


class TestUsuarioCreate:
    def test_valid(self):
        data = UsuarioCreate(
            nombre="Juan Pérez",
            email="juan@example.com",
            password="secret123",
        )
        assert data.nombre == "Juan Pérez"
        assert data.telefono is None

    def test_missing_email(self):
        with pytest.raises(ValidationError):
            UsuarioCreate(nombre="Juan", password="123")

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            UsuarioCreate(
                nombre="Juan",
                email="no-es-un-email",
                password="123",
            )


class TestLoginSchema:
    def test_valid(self):
        data = LoginSchema(email="test@test.com", password="pass")
        assert data.email == "test@test.com"

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            LoginSchema(email="invalido", password="pass")


class TestCategoriaCreate:
    def test_valid_without_descripcion(self):
        data = CategoriaCreate(nombre="Puertas")
        assert data.nombre == "Puertas"
        assert data.descripcion is None

    def test_valid_with_descripcion(self):
        data = CategoriaCreate(nombre="Puertas", descripcion="Puertas metálicas")
        assert data.descripcion == "Puertas metálicas"

    def test_missing_nombre(self):
        with pytest.raises(ValidationError):
            CategoriaCreate()


class TestObraCreate:
    def test_valid(self):
        data = ObraCreate(
            categoria_id=1,
            titulo="Puerta principal",
            destacado=True,
        )
        assert data.titulo == "Puerta principal"
        assert data.destacado is True

    def test_default_destacado(self):
        data = ObraCreate(categoria_id=1, titulo="Obra simple")
        assert data.destacado is False


class TestProductoCreate:
    def test_valid(self):
        data = ProductoCreate(
            nombre="Tornillo M8",
            precio=Decimal("12.50"),
        )
        assert data.nombre == "Tornillo M8"
        assert data.stock == 0
        assert data.disponible is True

    def test_invalid_precio(self):
        with pytest.raises(ValidationError):
            ProductoCreate(nombre="Test", precio="no es número")


class TestCotizacionCreate:
    def test_valid(self):
        data = CotizacionCreate(
            nombre_cliente="Carlos",
            telefono="3001234567",
            email="carlos@example.com",
            tipo_trabajo="Baranda",
            descripcion="Baranda para balcón",
        )
        assert data.usuario_id is None

    def test_with_usuario(self):
        data = CotizacionCreate(
            nombre_cliente="Carlos",
            telefono="3001234567",
            email="carlos@example.com",
            tipo_trabajo="Baranda",
            descripcion="Baranda para balcón",
            usuario_id=5,
        )
        assert data.usuario_id == 5
