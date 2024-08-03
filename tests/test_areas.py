import random
from tests.test_main import client


def test_create_area():
    response = client.post("/api/areas/", json={"name": "test_area", "camera_id": 1})
    assert response.status_code == 201
    assert response.json()["name"] == "test_area"


def test_create_area2():
    response = client.post("/api/areas/", json={"name": "test_area2", "camera_id": 1})
    print(response.json()["localtime"])
    assert response.status_code == 201
    assert response.json()["name"] == "test_area2"


def test_create_area_camera_not_found():
    response = client.post("/api/areas/", json={"name": "test_area2", "camera_id": 1222})
    assert response.status_code == 404


def test_create_area_with_algoparam():
    def random_score_thresh():
        return random.uniform(0.6, 0.9)

    response = client.post(
        "/api/areas/",
        json={
            "name": "test_area1",
            "camera_id": random.randint(1,4),
            "algoparam": {
                "eventtype_ids": "['1201','1202','1401','1501','2101', '2102','3101','1402','1502','1311']",
                "nms_thresh": random.uniform(0.6, 0.9),
                "people_score_thresh": random.uniform(0.6, 0.9),
                "face_score_thresh": random.uniform(0.6, 0.9),
                "head_score_thresh": random.uniform(0.6, 0.9),
                "helmet_score_thresh": random.uniform(0.6, 0.9),
                "fire_score_thresh": random.uniform(0.6, 0.9),
                "water_score_thresh": random.uniform(0.6, 0.9),
                "falldown_score_thresh": random.uniform(0.6, 0.9),
                "cross_line": "['50','500','1800','500']",
                "cross_direction": "['0','0','1920','1080']",
                "iou_cost_weight": random.uniform(0.6, 0.9),
                "cost_th": random.uniform(0.6, 0.9),
                "max_mismatch_times":random.randint(5,10)
            },
        },
    )
    assert response.status_code == 201


def test_create_area_failure():
    response = client.post("/api/areas/", json={"name": "test_area"})
    assert response.status_code == 422


def test_get_areas():
    response = client.get("/api/areas/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_area():
    response = client.get("/api/areas/2")
    assert response.status_code == 200
    assert response.json()["id"] == 2


def test_get_areas():
    response = client.get("/api/areas/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_areas_by_camera_id():
    response = client.get("/api/areas/?camera_id=1")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_area_not_found():
    response = client.get("/api/areas/9999")
    assert response.status_code == 404
