from datetime import datetime, timedelta

import pytz


def create_table(client, name="Test Table"):
    response = client.post(
        "/v1/tables/", json={"name": name, "seats": 4, "location": "Main hall"}
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_reservation(
    client, table_id, start_time, customer_name="Test User", duration=60
):
    return client.post(
        "/v1/reservations/",
        json={
            "customer_name": customer_name,
            "table_id": table_id,
            "reservation_time": start_time.isoformat(),
            "duration_minutes": duration,
        },
    )


def test_create_reservation(client):
    table_id = create_table(client, "Table 1")

    reservation_time = datetime.now(pytz.utc) + timedelta(hours=1)
    response = create_reservation(
        client, table_id, reservation_time, customer_name="John Doe"
    )
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["table_id"] == table_id


def test_get_reservations(client):
    response = client.get("/v1/reservations/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_delete_reservation(client):
    table_id = create_table(client, "Table 4")

    reservation_time = datetime.now(pytz.utc) + timedelta(hours=2)
    response = create_reservation(client, table_id, reservation_time)
    assert response.status_code == 201


def test_conflict_reservation(client):
    table_id = create_table(client)
    start_time = datetime.now(pytz.utc) + timedelta(hours=1)

    res1 = create_reservation(client, table_id, start_time)
    assert res1.status_code == 201

    res2 = create_reservation(client, table_id, start_time + timedelta(minutes=30))
    assert res2.status_code == 409
    assert "already reserved" in res2.json()["detail"]


def test_reservation_in_the_past(client):
    table_id = create_table(client, "Past Table")
    past_time = datetime.now(pytz.utc) - timedelta(hours=1)

    res = create_reservation(client, table_id, past_time)
    assert res.status_code == 422 or res.status_code == 400
    assert "must be in the future" in str(res.json())


def test_delete_nonexistent_reservation(client):
    res = client.delete("/v1/reservations/99999")
    assert res.status_code == 404
    assert "not found" in res.json()["detail"].lower()
