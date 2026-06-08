import pytest


class TestCategorias:
    def test_listar_categorias_vacio(self, client):
        response = client.get("/api/portafolio/categorias")
        assert response.status_code == 200
        assert response.json() == []

    def test_crear_categoria(self, client):
        response = client.post("/api/portafolio/categorias", json={
            "nombre": "Puertas",
            "descripcion": "Puertas metálicas y artísticas",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Puertas"
        assert "id" in data

    def test_crear_categoria_sin_descripcion(self, client):
        response = client.post("/api/portafolio/categorias", json={
            "nombre": "Barandas",
        })
        assert response.status_code == 201
        assert response.json()["descripcion"] is None

    def test_listar_categorias_con_datos(self, client):
        client.post("/api/portafolio/categorias", json={"nombre": "Puertas"})
        client.post("/api/portafolio/categorias", json={"nombre": "Barandas"})
        response = client.get("/api/portafolio/categorias")
        assert len(response.json()) == 2


class TestObras:
    def test_crear_obra(self, client):
        cat = client.post("/api/portafolio/categorias", json={"nombre": "Puertas"}).json()
        response = client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Puerta principal moderna",
            "descripcion": "Puerta de hierro forjado",
            "destacado": True,
        })
        assert response.status_code == 201
        data = response.json()
        assert data["titulo"] == "Puerta principal moderna"
        assert data["destacado"] is True
        assert data["categoria"]["nombre"] == "Puertas"

    def test_listar_obras_vacio(self, client):
        response = client.get("/api/portafolio/obras")
        assert response.status_code == 200
        assert response.json() == []

    def test_listar_obras_con_datos(self, client):
        cat = client.post("/api/portafolio/categorias", json={"nombre": "Rejas"}).json()
        client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Reja colonial",
        })
        client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Reja moderna",
        })
        response = client.get("/api/portafolio/obras")
        assert len(response.json()) == 2

    def test_obtener_obra_por_id(self, client):
        cat = client.post("/api/portafolio/categorias", json={"nombre": "Barandas"}).json()
        creada = client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Baranda balcón",
        }).json()
        response = client.get(f"/api/portafolio/obras/{creada['id']}")
        assert response.status_code == 200
        assert response.json()["titulo"] == "Baranda balcón"

    def test_obtener_obra_no_existe(self, client):
        response = client.get("/api/portafolio/obras/9999")
        assert response.status_code == 404

    def test_actualizar_obra(self, client):
        cat = client.post("/api/portafolio/categorias", json={"nombre": "Puertas"}).json()
        obra = client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Puerta vieja",
        }).json()
        response = client.put(f"/api/portafolio/obras/{obra['id']}", json={
            "categoria_id": cat["id"],
            "titulo": "Puerta renovada",
        })
        assert response.status_code == 200
        assert response.json()["titulo"] == "Puerta renovada"

    def test_eliminar_obra(self, client):
        cat = client.post("/api/portafolio/categorias", json={"nombre": "Rejas"}).json()
        obra = client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Reja a eliminar",
        }).json()
        response = client.delete(f"/api/portafolio/obras/{obra['id']}")
        assert response.status_code == 204

    def test_eliminar_obra_no_existe(self, client):
        response = client.delete("/api/portafolio/obras/9999")
        assert response.status_code == 404

    def test_filtrar_obras_por_categoria(self, client):
        cat1 = client.post("/api/portafolio/categorias", json={"nombre": "Puertas"}).json()
        cat2 = client.post("/api/portafolio/categorias", json={"nombre": "Barandas"}).json()
        client.post("/api/portafolio/obras", json={
            "categoria_id": cat1["id"],
            "titulo": "Puerta",
        })
        client.post("/api/portafolio/obras", json={
            "categoria_id": cat2["id"],
            "titulo": "Baranda",
        })
        response = client.get(f"/api/portafolio/obras?categoria_id={cat1['id']}")
        assert len(response.json()) == 1
        assert response.json()[0]["titulo"] == "Puerta"

    def test_filtrar_obras_destacadas(self, client):
        cat = client.post("/api/portafolio/categorias", json={"nombre": "Puertas"}).json()
        client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Destacada",
            "destacado": True,
        })
        client.post("/api/portafolio/obras", json={
            "categoria_id": cat["id"],
            "titulo": "Normal",
        })
        response = client.get("/api/portafolio/obras?destacado=true")
        assert len(response.json()) == 1
        assert response.json()[0]["titulo"] == "Destacada"
