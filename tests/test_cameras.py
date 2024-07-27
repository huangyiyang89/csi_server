from tests.test_main import client
from models.camera import Camera, CameraPublic, CameraCreate, CameraUpdate, CameraWithDatas


def test_create_camera():
    response = client.post("/cameras", json={"name": "camera1", "ip_addr": "192.168.1.1", "mac": "00:11:22:33:44:55", "frame_height": 1080, "frame_width": 1920})
    assert response.status_code == 201
    assert response.json()["name"] == "camera1"
    assert response.json()["ip_addr"] == "192.168.1.1"
    assert response.json()["mac"] == "00:11:22:33:44:55"
    assert response.json()["frame_height"] == 1080
    assert response.json()["frame_width"] == 1920
    assert response.json()["state"] == 0


def test_create_camera_failure():
    response = client.post("/cameras", json={"name": "camera1"})
    assert response.status_code == 422

def test_get_camera():
    response = client.get("/cameras/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_camera_failure():
    response = client.get("/cameras/11111")
    assert response.status_code == 404

def test_get_cameras():
    response = client.get("/cameras")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1