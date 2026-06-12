import pytest


class TestCategorias:
    def test_listar_categorias_vacio(self, client):
        response = client.get("/api/portafolio/categorias")
        assert response.status_code == 200
        assert response.json() == []

    def test_crear_categoria(self, client, auth_headers):
        response = client.post("/api/portafolio/categorias", json={
            "nombre": "Puertas",
            "descripcion": "Puertas metálicas y artísticas",
        }, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Puertas"
        assert "id" in data

    def test_crear_categoria_sin_descripcion(self, client, auth_headers):
        response = client.post("/api/portafolio/categorias", json={
            "nombre": "Barandas",
        }, headers=auth_headers)
        assert response.status_code == 201
        assert response.json()["descripcion"] is None

    def test_listar_categorias_con_datos(self, client, auth_headers):
        client.post("/api/portafolio/categorias", json={"nombre": "Puertas"}, headers=auth_headers)
        client.post("/api/portafolio/categorias", json={"nombre": "Barandas"}, headers=auth_headers)
        response = client.get("/api/portafolio/categorias")
        assert len(response.json()) == 2


class TestObras:
    def test_crear_obra(self, client, auth_headers):
        cat = client.post("/api/portafolio/categorias", json={"nombre": "Puertas"}, headers=auth_headers).json()
        response = client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Puerta principal moderna",
            "descripcion": "Puerta de hierro forjado",
            "destacado": True,
        }, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["titulo"] == "Puerta principal moderna"
        assert data["destacado"] is True
        assert data["categoria"]["nombre"] == "Puertas"

    def test_listar_obras_vacio(self, client):
        response = client.get("/api/portafolio/obras")
        assert response.status_code == 200
        assert response.json() == []

    def test_listar_obras_con_datos(self, client, auth_headers):
        cat = client.post("/api/portafolio/categorias", json={"nombre": "Rejas"}, headers=auth_headers).json()
        client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Reja colonial",
        }, headers=auth_headers)
        client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Reja moderna",
        }, headers=auth_headers)
        response = client.get("/api/portafolio/obras")
        assert len(response.json()) == 2

    def test_obtener_obra_por_id(self, client, auth_headers):
        cat = client.post("/api/portafolio/categorias", json={"nombre": "Barandas"}, headers=auth_headers).json()
        creada = client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Baranda balcón",
        }, headers=auth_headers).json()
        response = client.get(f"/api/portafolio/obras/{creada['id']}")
        assert response.status_code == 200
        assert response.json()["titulo"] == "Baranda balcón"

    def test_obtener_obra_no_existe(self, client):
        response = client.get("/api/portafolio/obras/9999")
        assert response.status_code == 404

    def test_actualizar_obra(self, client, auth_headers):
        cat = client.post("/api/portafolio/categorias", json={"nombre": "Puertas"}, headers=auth_headers).json()
        obra = client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Puerta vieja",
        }, headers=auth_headers).json()
        response = client.put(f"/api/portafolio/obras/{obra['id']}", json={
            "categoria_id": cat["id"],
            "titulo": "Puerta renovada",
        }, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["titulo"] == "Puerta renovada"

    def test_eliminar_obra(self, client, auth_headers):
        cat = client.post("/api/portafolio/categorias", json={"nombre": "Rejas"}, headers=auth_headers).json()
        obra = client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Reja a eliminar",
        }, headers=auth_headers).json()
        response = client.delete(f"/api/portafolio/obras/{obra['id']}", headers=auth_headers)
        assert response.status_code == 204

    def test_eliminar_obra_no_existe(self, client, auth_headers):
        response = client.delete("/api/portafolio/obras/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_filtrar_obras_por_categoria(self, client, auth_headers):
        cat1 = client.post("/api/portafolio/categorias", json={"nombre": "Puertas"}, headers=auth_headers).json()
        cat2 = client.post("/api/portafolio/categorias", json={"nombre": "Barandas"}, headers=auth_headers).json()
        client.post("/api/portafolio/obras", json={
            "categoria_id": cat1["id"],
            "titulo": "Puerta",
        }, headers=auth_headers)
        client.post("/api/portafolio/obras", json={
            "categoria_id": cat2["id"],
            "titulo": "Baranda",
        }, headers=auth_headers)
        response = client.get(f"/api/portafolio/obras?categoria_id={cat1['id']}")
        assert len(response.json()) == 1
        assert response.json()[0]["titulo"] == "Puerta"

    def test_filtrar_obras_destacadas(self, client, auth_headers):
        cat = client.post("/api/portafolio/categorias", json={"nombre": "Puertas"}, headers=auth_headers).json()
        client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Destacada",
            "destacado": True,
        }, headers=auth_headers)
        client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Normal",
        }, headers=auth_headers)
        response = client.get("/api/portafolio/obras?destacado=true")
        assert len(response.json()) == 1
        assert response.json()[0]["titulo"] == "Destacada"
