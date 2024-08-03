from tests.test_main import client

def test_get_events():
    response = client.get("/api/events")
    assert response.status_code == 200

def test_gen_events():
    response = client.get("/api/events/gen")
    assert response.status_code == 200
