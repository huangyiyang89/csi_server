import os
import platform
import time
import psutil
import random
import socket
import telnetlib
import asyncio
from scapy.layers.l2 import ARP, Ether, srp
from paramiko import SSHClient, AutoAddPolicy
from multiprocessing import Process



def now():
    return time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def get_cpu_percent():
    return psutil.cpu_percent()


def get_memory_percent():
    memory = psutil.virtual_memory()
    return memory.percent


def get_disk_percent():
    disk_usage = psutil.disk_usage("/")
    return disk_usage.percent


def get_npu_percent():
    return random.randint(30, 80)


def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def get_uptime():
    """运行时长"""
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds
    except FileNotFoundError:
        return 0


def get_mac(ip):

    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=False)[0]
    if len(result) > 0:
        return result[0][1].hwsrc.lower()
    else:
        return None


def scan_network():
    arp = ARP(pdst="192.168.0.1/24")
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]
    devices = []
    for sent, received in result:
        devices.append({"ip": received.psrc, "mac": received.hwsrc})
    return devices


def get_local_mac():
    nics = psutil.net_if_addrs()
    for nic_name, nic_addrs in nics.items():
        #if "eth" in nic_name or "en" in nic_name:
            for addr in nic_addrs:
                if addr.family == psutil.AF_LINK:
                    mac = addr.address
                    return mac.replace("-", ":").lower()
    print("获取本机mac地址失败！")
    return "ff:ff:ff:ff:ff:ff"


async def check_status(ip, port=80, timeout=0.1):
    loop = asyncio.get_event_loop()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setblocking(False)
        try:
            await asyncio.wait_for(loop.sock_connect(sock, (ip, port)), timeout)
            return 1
        except (OSError, asyncio.TimeoutError):
            return 0


def reboot():
    try:
        current_os = platform.system()
        if current_os == "Windows":
            os.system("shutdown /r /t 0")
        elif current_os == "Linux" or current_os == "Darwin":
            os.system("sudo reboot")
        else:
            print("Not supported system")
    except Exception as e:
        print(f"Restart error: {e}")


def ssh_port_forwarding(
    remote_ip, remote_port, local_port, username, password, timeout
):
    try:
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(remote_ip, port=22, username=username, password=password)

        transport = client.get_transport()
        transport.request_port_forward("", local_port, remote_ip, remote_port)

        print(f"SSH forwarding {remote_ip}:{remote_port} to local:{local_port} success")

        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                break
            transport.accept(1000)

    except Exception as e:
        print(f"Except ssh error: {e}")
    finally:
        client.close()


def start_ssh_process(remote_ip, remote_port, local_port, username, password, timeout):
    process = Process(
        target=ssh_port_forwarding,
        args=(remote_ip, remote_port, local_port, username, password, timeout),
    )
    process.start()
    return process
