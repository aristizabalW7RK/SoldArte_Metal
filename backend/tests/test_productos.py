from decimal import Decimal


class TestProductos:
    def test_listar_productos_vacio(self, client):
        response = client.get("/api/productos")
        assert response.status_code == 200
        assert response.json() == []

    def test_crear_producto(self, client, auth_headers):
        response = client.post("/api/productos", json={
            "nombre": "Tornillo M8x30",
            "precio": 12.50,
            "stock": 100,
        }, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Tornillo M8x30"
        assert float(data["precio"]) == 12.50
        assert data["stock"] == 100
        assert data["disponible"] is True

    def test_crear_producto_sin_precio(self, client, auth_headers):
        response = client.post("/api/productos", json={
            "nombre": "Sin precio",
        }, headers=auth_headers)
        assert response.status_code == 422

    def test_listar_productos_con_datos(self, client, auth_headers):
        client.post("/api/productos", json={"nombre": "A", "precio": 10}, headers=auth_headers)
        client.post("/api/productos", json={"nombre": "B", "precio": 20}, headers=auth_headers)
        response = client.get("/api/productos")
        assert len(response.json()) == 2

    def test_obtener_producto_por_id(self, client, auth_headers):
        creado = client.post("/api/productos", json={
            "nombre": "Candado",
            "precio": 25.00,
        }, headers=auth_headers).json()
        response = client.get(f"/api/productos/{creado['id']}")
        assert response.status_code == 200
        assert response.json()["nombre"] == "Candado"

    def test_obtener_producto_no_existe(self, client):
        response = client.get("/api/productos/9999")
        assert response.status_code == 404

    def test_actualizar_producto(self, client, auth_headers):
        creado = client.post("/api/productos", json={
            "nombre": "Nombre viejo",
            "precio": 10,
        }, headers=auth_headers).json()
        response = client.put(f"/api/productos/{creado['id']}", json={
            "nombre": "Nombre nuevo",
            "precio": 15.50,
        }, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["nombre"] == "Nombre nuevo"
        assert float(response.json()["precio"]) == 15.50

    def test_eliminar_producto(self, client, auth_headers):
        creado = client.post("/api/productos", json={
            "nombre": "A eliminar",
            "precio": 5,
        }, headers=auth_headers).json()
        response = client.delete(f"/api/productos/{creado['id']}", headers=auth_headers)
        assert response.status_code == 204

    def test_eliminar_producto_no_existe(self, client, auth_headers):
        response = client.delete("/api/productos/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_filtrar_solo_disponibles(self, client, auth_headers):
        client.post("/api/productos", json={
            "nombre": "Disponible",
            "precio": 10,
            "disponible": True,
        }, headers=auth_headers)
        client.post("/api/productos", json={
            "nombre": "No disponible",
            "precio": 20,
            "disponible": False,
        }, headers=auth_headers)
        response = client.get("/api/productos?solo_disponibles=true")
        assert len(response.json()) == 1
        assert response.json()[0]["nombre"] == "Disponible"

    def test_incluir_no_disponibles(self, client, auth_headers):
        client.post("/api/productos", json={
            "nombre": "Disponible",
            "precio": 10,
            "disponible": True,
        }, headers=auth_headers)
        client.post("/api/productos", json={
            "nombre": "No disponible",
            "precio": 20,
            "disponible": False,
        }, headers=auth_headers)
        response = client.get("/api/productos?solo_disponibles=false")
        assert len(response.json()) == 2
