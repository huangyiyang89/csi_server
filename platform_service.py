import hashlib
import requests

import time
import base64
from database import get_session
from sqlmodel import Session, select
from models.event import Event
from models.camera import Camera
from models.area import Area

import util


api_host = "http://81.70.52.233/api/aiot/"

mac = "11:22:33:44:55:66"
secret = "112233445566AIoT!@#123"


def sign(api_key="112233445566", secret="112233445566AIoT!@#123"):
    timestamp = str(int(time.time()))
    encoded_str = (api_key + timestamp + secret).encode("utf-8")
    return hashlib.md5(encoded_str).hexdigest() + api_key + timestamp


def get_tasks():
    """_summary_

    Returns:
        _type_: task[] {"action":"reboot","params":{host,port,timeout}}
    """
    try:
        url = api_host + "task" + f"?sign={sign()}"
        response = requests.post(url)
        response.raise_for_status()
        data = response.json()
        print("get tasks success, data:", data)
        return data["data"]["tasks"]
    except requests.exceptions.RequestException as e:
        print("get tasks error:", e)
        return []


def upload_status():
    try:
        url = api_host + "status" + f"?sign={sign()}"

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
        }
        response = requests.post(url=url, json=upload_data)
        response.raise_for_status()
        print("upload status success, response:", upload_data, response.json())
    except requests.exceptions.RequestException as e:
        print("upload status error:", e)


def upload_events():
    url = api_host + "event" + f"?sign={sign()}"
    try:
        for session in get_session():
            events = session.exec(select(Event).where(Event.uploaded == False)).all()
            if len(events) == 0:
                print("no event is not uploaded")
                return
            
            print("waiting for upload events count:", len(events))
            events_json_list = []
            for event in events:
                with open("frontend/" + event.image_url, "rb") as image_file:
                    data = image_file.read()
                encoded_string = "data:image/jpeg;base64," + base64.b64encode(
                    data
                ).decode("utf-8")
                upload_event_data = {
                    "camera": "11:22:33:44:55:77",
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
                print("event upload success:", event, response.json())

            # response = requests.post(url, json={"events": events_json_list})
            # response.raise_for_status()

            # for event in events:
            #     event.uploaded = True
            # session.commit()

    except requests.exceptions.RequestException as e:
        print("event upload fail, error:", e)
