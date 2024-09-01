import psutil
import random
import socket
from scapy.layers.l2 import ARP, Ether, srp

def get_cpu_percent():
    return psutil.cpu_percent()

def get_memory_percent():
    memory = psutil.virtual_memory()
    return memory.percent
def get_disk_percent():
    disk_usage = psutil.disk_usage('/')
    return disk_usage.percent


def get_npu_percent():
    return random.randint(30,80)


def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds
    except FileNotFoundError:
        return 0
    
def get_mac(ip):

    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=False)[0]
    if len(result) > 0:
        return result[0][1].hwsrc
    else:
        return None
    
def scan_network():
    arp = ARP(pdst='192.168.0.1/24')
    ether = Ether(dst='ff:ff:ff:ff:ff:ff')
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices