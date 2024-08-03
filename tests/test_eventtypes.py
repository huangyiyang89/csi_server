from tests.test_main import client


def test_get_eventtypes():
    response = client.get("/api/eventtypes")
    assert response.status_code == 200
    assert response.json()[9]["name"] == "抽烟检测"
    assert len(response.json()) == 10

