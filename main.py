from requests.structures import CaseInsensitiveDict
import requests
import logging
import sys
import csv
import time

logging.basicConfig(filename='app.log', filemode='a',
                    format='%(levelname)s:%(asctime)s:%(message)s')

# Config
DA_URL = "https://directadmin:2222"
DA_USERNAME = "USERNAME"
DA_PASSWORD = "PASSWORD"
MAIL_DOMAIN = "example.com"
QUOTA = 10
token = "" # You can copy the session token from your saved cookies by logging in to your DA panel


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def getToken():
    url = f"{DA_URL}/CMD_LOGIN"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    data = f"username={DA_USERNAME}&password={DA_PASSWORD}&json=yes"
    resp = requests.post(url, headers=headers, data=data)
    if resp.status_code != 200:
        sys.exit("Directadmin Authentication Failed")
    return find_between(resp.headers["Set-Cookie"], "session=", ";")


if token == "":
    token = getToken()

with open('accounts.csv', newline='') as csvfile:
    emails = list(csv.reader(csvfile))

for i in range(1, len(emails)):
    url = f"{DA_URL}/CMD_API_POP?action=create&domain={MAIL_DOMAIN}&user={emails[i][0]}&passwd={emails[i][1]}&quota={QUOTA}&redirect=no"
    headers = CaseInsensitiveDict()
    headers["Connection"] = "keep-alive"
    headers["Referer"] = DA_URL
    headers["Cookie"] = f"session={token}"
    resp = requests.post(url, headers=headers)
    if resp.status_code == 200:
        if resp.content.decode("utf-8").startswith('error=1'):
            if resp.content == b"error=1&text=Unable%20to%20create%20email%20account&details=That%20user%20already%20exists%3Cbr%3E%0A":
                logging.error(
                    f"{i}-{emails[i][0]}-{emails[i][1]}:duplicatedUser")
            else:
                logging.error(
                    f"{i}-{emails[i][0]}-{emails[i][1]}:{resp.content}")
                sys.exit(
                    f"Error: {i}-{emails[i][0]}-{emails[i][1]}:{resp.content}")
        else:
            print(
                f"{i}. Account {emails[i][0]}@{MAIL_DOMAIN} successfully created")
