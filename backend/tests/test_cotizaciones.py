import pytest


class TestCotizaciones:
    def test_crear_cotizacion(self, client):
        response = client.post("/api/cotizaciones", json={
            "nombre_cliente": "Carlos López",
            "telefono": "3001234567",
            "email": "carlos@example.com",
            "tipo_trabajo": "Baranda",
            "descripcion": "Baranda para balcón de 3 metros",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["nombre_cliente"] == "Carlos López"
        assert data["estado"] == "nueva"
        assert "id" in data

    def test_crear_cotizacion_con_usuario(self, client):
        user = client.post("/api/auth/registro", json={
            "nombre": "Juan",
            "email": "jcot@example.com",
            "password": "123",
        }).json()
        response = client.post("/api/cotizaciones", json={
            "nombre_cliente": "Juan Pérez",
            "telefono": "3007654321",
            "email": "jcot@example.com",
            "tipo_trabajo": "Puerta",
            "descripcion": "Puerta principal",
            "usuario_id": user["id"],
        })
        assert response.status_code == 201
        assert response.json()["usuario_id"] == user["id"]

    def test_listar_cotizaciones(self, client):
        client.post("/api/cotizaciones", json={
            "nombre_cliente": "A",
            "telefono": "1",
            "email": "a@a.com",
            "tipo_trabajo": "Reja",
            "descripcion": "Reja ventana",
        })
        client.post("/api/cotizaciones", json={
            "nombre_cliente": "B",
            "telefono": "2",
            "email": "b@b.com",
            "tipo_trabajo": "Puerta",
            "descripcion": "Puerta entrada",
        })
        response = client.get("/api/cotizaciones")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_filtrar_cotizaciones_por_estado(self, client):
        client.post("/api/cotizaciones", json={
            "nombre_cliente": "A",
            "telefono": "1",
            "email": "a@a.com",
            "tipo_trabajo": "Reja",
            "descripcion": "Reja ventana",
        })
        client.post("/api/cotizaciones", json={
            "nombre_cliente": "B",
            "telefono": "2",
            "email": "b@b.com",
            "tipo_trabajo": "Puerta",
            "descripcion": "Puerta entrada",
        })
        response = client.get("/api/cotizaciones?estado=nueva")
        assert len(response.json()) == 2

    def test_cambiar_estado_cotizacion(self, client):
        cot = client.post("/api/cotizaciones", json={
            "nombre_cliente": "Test",
            "telefono": "123",
            "email": "test@test.com",
            "tipo_trabajo": "Ventana",
            "descripcion": "Ventana hierro",
        }).json()
        response = client.patch(f"/api/cotizaciones/{cot['id']}/estado?estado=en_revision")
        assert response.status_code == 200
        assert response.json()["mensaje"] == "Estado actualizado"

    def test_cambiar_estado_invalido(self, client):
        cot = client.post("/api/cotizaciones", json={
            "nombre_cliente": "Test",
            "telefono": "123",
            "email": "test@test.com",
            "tipo_trabajo": "Ventana",
            "descripcion": "Ventana hierro",
        }).json()
        response = client.patch(f"/api/cotizaciones/{cot['id']}/estado?estado=inexistente")
        assert response.status_code == 400

    def test_cotizacion_no_encontrada(self, client):
        response = client.patch("/api/cotizaciones/9999/estado?estado=cerrada")
        assert response.status_code == 404


class TestFavoritos:
    def test_agregar_favorito(self, client):
        user = client.post("/api/auth/registro", json={
            "nombre": "Fav User",
            "email": "fav@example.com",
            "password": "123",
        }).json()
        prod = client.post("/api/productos", json={
            "nombre": "Producto favorito",
            "precio": 100,
        }).json()
        response = client.post(f"/api/usuarios/{user['id']}/favoritos/{prod['id']}")
        assert response.status_code == 201
        assert response.json()["producto"]["id"] == prod["id"]

    def test_agregar_favorito_duplicado(self, client):
        user = client.post("/api/auth/registro", json={
            "nombre": "Fav2",
            "email": "fav2@example.com",
            "password": "123",
        }).json()
        prod = client.post("/api/productos", json={
            "nombre": "Producto",
            "precio": 50,
        }).json()
        client.post(f"/api/usuarios/{user['id']}/favoritos/{prod['id']}")
        response = client.post(f"/api/usuarios/{user['id']}/favoritos/{prod['id']}")
        assert response.status_code == 400

    def test_listar_favoritos(self, client):
        user = client.post("/api/auth/registro", json={
            "nombre": "Fav3",
            "email": "fav3@example.com",
            "password": "123",
        }).json()
        prod1 = client.post("/api/productos", json={"nombre": "P1", "precio": 10}).json()
        prod2 = client.post("/api/productos", json={"nombre": "P2", "precio": 20}).json()
        client.post(f"/api/usuarios/{user['id']}/favoritos/{prod1['id']}")
        client.post(f"/api/usuarios/{user['id']}/favoritos/{prod2['id']}")
        response = client.get(f"/api/usuarios/{user['id']}/favoritos")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_eliminar_favorito(self, client):
        user = client.post("/api/auth/registro", json={
            "nombre": "Fav4",
            "email": "fav4@example.com",
            "password": "123",
        }).json()
        prod = client.post("/api/productos", json={"nombre": "P", "precio": 5}).json()
        client.post(f"/api/usuarios/{user['id']}/favoritos/{prod['id']}")
        response = client.delete(f"/api/usuarios/{user['id']}/favoritos/{prod['id']}")
        assert response.status_code == 204

    def test_eliminar_favorito_no_existe(self, client):
        response = client.delete("/api/usuarios/1/favoritos/999")
        assert response.status_code == 404
