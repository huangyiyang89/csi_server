import hashlib
import requests
import time
import base64
from database import get_session
from sqlmodel import select
from models.event import Event
from models.camera import Camera
from models.nvr import Nvr
import util
import config

def print_now(*args):
    print(util.now(), *args)

def sign():
    if "config.key" not in locals() or "config.key" not in globals() or config.key == "":
        key = util.get_local_mac().replace(":","").lower()
        secret = key + "AIoT!@#123"
    else:
        key = config.key
        secret = config.secret
    try:
        timestamp =  str(int(time.time()))
        encoded_str = (key + timestamp + secret).encode("utf-8")
        sig = hashlib.md5(encoded_str).hexdigest() + key + timestamp
    except Exception as e:
        print_now("Sign error:", e)
        sig = ""
    return sig


def get_tasks():
    try:
        url = config.api_host + "task" + f"?sign={sign()}"
        response = requests.post(url)
        response.raise_for_status()
        data = response.json()
        print_now("Fetch tasks success:", data["data"])
        return data["data"]["tasks"]
    except requests.exceptions.RequestException as e:
        print_now("Fetch tasks error:", e)
        return []


def upload_status():
    try:
        url = config.api_host + "status" + f"?sign={sign()}"

        cameras_to_upload = []
        nvrs_to_upload = []
        for session in get_session():
            cameras = session.exec(select(Camera)).all()
            for camera in cameras:
                camera_to_upload = {
                    "id": camera.mac,
                    "ip": camera.ip_addr,
                    "ch": camera.nvr_channel if camera.nvr else "",
                    "status": camera.state,
                    "nvr": camera.nvr.mac if camera.nvr else "",
                    "brand": camera.brand,
                }
                cameras_to_upload.append(camera_to_upload)

            nvrs = session.exec(select(Nvr)).all()
            for nvr in nvrs:
                nvr_to_upload = {
                    "id": nvr.mac,
                    "ip": nvr.ip,
                    "status": nvr.state,
                    "brand": nvr.brand,
                }
                nvrs_to_upload.append(nvr_to_upload)

        upload_data = {
            "ip": util.get_ip_address(),
            "version": "v2.3.5_20240501",
            "timezone": "+08:00",
            "uptime": util.get_uptime(),
            "status": {
                "cpu": util.get_cpu_percent(),
                "ram": util.get_memory_percent(),
                "disk": util.get_disk_percent(),
                "npu": util.get_npu_percent(),
            },
            "cameras": cameras_to_upload,
            "nvr": nvrs_to_upload,
        }
        response = requests.post(url=url, json=upload_data)
        response.raise_for_status()
        print_now("Upload status success, data:", upload_data, "response:",response.json())
    except requests.exceptions.RequestException as e:
        print_now("Upload status error:", e)


def upload_events():
    url = config.api_host + "event" + f"?sign={sign()}"
    try:
        for session in get_session():
            events = session.exec(select(Event).where(Event.uploaded == False)).all()
            if len(events) == 0:
                print_now("All events are uploaded.")
                return

            print_now("There are",len(events),"events waiting for upload ...")
            events_json_list = []
            for event in events:
                with open("frontend/" + event.image_url, "rb") as image_file:
                    data = image_file.read()
                encoded_string = "data:image/jpeg;base64," + base64.b64encode(
                    data
                ).decode("utf-8")
                upload_event_data = {
                    "camera": event.camera.mac if event.camera else "",
                    "area": "all",
                    "event": event.eventtype.id,
                    "timestamp": event.timestamp,
                    "image": encoded_string,
                }
                events_json_list.append(upload_event_data)
                response = requests.post(url, json={"events": [upload_event_data]})
                response.raise_for_status()
                event.uploaded = True
                session.commit()
                print_now("Event upload success, data:", upload_event_data, "response:",response.json())

            # 批量上传, 数据过大失败
            # response = requests.post(url, json={"events": events_json_list})
            # response.raise_for_status()

            # for event in events:
            #     event.uploaded = True
            # session.commit()

    except requests.exceptions.RequestException as e:
        print_now("Event upload fail, error:", e)

