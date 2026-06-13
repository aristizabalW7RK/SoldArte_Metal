import pytest


class TestRegistro:
    def test_registro_exitoso(self, client):
        response = client.post("/api/auth/registro", json={
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "password": "secret123",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Juan Pérez"
        assert data["email"] == "juan@example.com"
        assert "password" not in data
        assert "id" in data

    def test_registro_email_duplicado(self, client):
        client.post("/api/auth/registro", json={
            "nombre": "Juan",
            "email": "duplicado@example.com",
            "password": "123",
        })
        response = client.post("/api/auth/registro", json={
            "nombre": "Pedro",
            "email": "duplicado@example.com",
            "password": "456",
        })
        assert response.status_code == 400
        assert "registrado" in response.json()["detail"]

    def test_registro_sin_email(self, client):
        response = client.post("/api/auth/registro", json={
            "nombre": "Juan",
            "password": "123",
        })
        assert response.status_code == 422


class TestLogin:
    def test_login_exitoso(self, client):
        client.post("/api/auth/registro", json={
            "nombre": "Juan",
            "email": "login@example.com",
            "password": "miclave",
        })
        response = client.post("/api/auth/login", json={
            "email": "login@example.com",
            "password": "miclave",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "login@example.com"
        assert "id" in data
        assert "soldarte_token" in response.cookies

    def test_login_credenciales_invalidas(self, client):
        response = client.post("/api/auth/login", json={
            "email": "no@existe.com",
            "password": "x",
        })
        assert response.status_code == 401

    def test_login_password_incorrecto(self, client):
        client.post("/api/auth/registro", json={
            "nombre": "Juan",
            "email": "passincorrect@example.com",
            "password": "correcta",
        })
        response = client.post("/api/auth/login", json={
            "email": "passincorrect@example.com",
            "password": "incorrecta",
        })
        assert response.status_code == 401
