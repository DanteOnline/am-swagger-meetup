import datetime
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_post_event():
    payload = {
        "camera_id": "cam01",
        "event_type": "motion",
        "confidence": 0.85,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "location": "station1"
    }
    r = client.post("/events/", json=payload)
    assert r.status_code == 201
    assert r.json()["camera_id"] == payload["camera_id"]

def test_get_list():
    r = client.get("/events/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_get_detail():
    create = client.post("/events/", json={
        "camera_id": "cam02",
        "event_type": "face",
        "confidence": 0.91,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "location": "station2"
    }).json()
    r = client.get(f"/events/{create['id']}/")
    assert r.status_code == 200
    assert r.json()["id"] == create["id"]

    r = client.get("/events/666/")
    assert r.status_code == 404

def test_patch_event():
    event = client.post("/events/", json={
        "camera_id": "cam03",
        "event_type": "object",
        "confidence": 0.6,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "location": "station3"
    }).json()
    r = client.patch(f"/events/{event['id']}/", json={"confidence": 0.95})
    assert r.status_code == 200
    assert r.json()["confidence"] == 0.95

    r = client.patch("/events/666/", json={"confidence": 0.95})
    assert r.status_code == 404

def test_delete_event():
    event = client.post("/events/", json={
        "camera_id": "cam04",
        "event_type": "motion",
        "confidence": 0.4,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "location": "station4"
    }).json()
    r = client.delete(f"/events/{event['id']}/")
    assert r.status_code == 204
    r = client.get(f"/events/{event['id']}/")
    assert r.status_code == 404
    r = client.delete("/events/666/")
    assert r.status_code == 404

def test_put_event():
    # Сначала создаем событие
    response = client.post("/events/", json={
        "camera_id": "cam_put_test",
        "event_type": "object_detected",
        "confidence": 0.75,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "location": "street_77"
    })
    assert response.status_code == 201
    event = response.json()
    event_id = event["id"]

    # Полностью обновляем объект
    updated_data = {
        "camera_id": "cam_put_updated",
        "event_type": "face_detected",
        "confidence": 0.95,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "location": "updated_location"
    }

    put_response = client.put(f"/events/{event_id}/", json=updated_data)
    assert put_response.status_code == 200
    response_data = put_response.json()

    assert response_data["camera_id"] == updated_data["camera_id"]
    assert response_data["event_type"] == updated_data["event_type"]
    assert abs(response_data["confidence"] - updated_data["confidence"]) < 0.01
    assert response_data["location"] == updated_data["location"]

    put_response = client.put("/events/666/", json=updated_data)
    assert put_response.status_code == 404
