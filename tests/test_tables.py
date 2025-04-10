def test_create_table(client):
    response = client.post(
        "/v1/tables/", json={"name": "Table 1", "seats": 4, "location": "Window"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Table 1"
    assert data["seats"] == 4
    assert data["location"] == "Window"


def test_get_tables(client):
    response = client.get("/v1/tables/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_delete_table(client):
    response = client.post(
        "/v1/tables/", json={"name": "Table 2", "seats": 2, "location": "Terrace"}
    )
    assert response.status_code == 201
    table_id = response.json()["id"]

    response = client.delete(f"/v1/tables/{table_id}")
    assert response.status_code == 204

    response = client.get(f"/v1/tables/{table_id}")
    assert response.status_code == 404
