#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Requirements:
    * python 3.6+
    * requests https://pypi.org/project/requests/
    * envparse https://pypi.org/project/envparse/

Install them with:
pip install requests envparse

This script also requires a .env, which is a simple KEY=VALUE file, e.g.:

HOST=https://your.wallabag.host
USER_NAME=wallabag_user_name
PASSWORD=wallabag_password
CLIENT_ID=wallabag_api_client_id
CLIENT_SECRET=wallabag_api_client_secret
"""
import json
from typing import List
from urllib.parse import urljoin

import requests
from envparse import env

env.read_envfile()

HOST = env.str("HOST")
CLIENT_ID = env.str("CLIENT_ID")
CLIENT_SECRET = env.str("CLIENT_SECRET")
USER = env.str("USER_NAME")
PASS = env.str("PASSWORD")


def get_bearer_token() -> str:
    endpoint = "/oauth/v2/token"
    data = {
        "grant_type": "password",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": USER,
        "password": PASS,
    }
    url = urljoin(HOST, endpoint)
    response = requests.post(url, json=data)
    error = f"Expected 200 OK but got {response.status_code} from {url}"
    assert response.status_code == 200, error

    return response.json()["access_token"]


def get_entries(token: str, *, per_page: int = 1000) -> dict:
    endpoint = f"/api/entries.json"
    params = {
        "perPage": per_page,
    }
    headers = {"Authorization": f"Bearer {token}"}
    url = urljoin(HOST, endpoint)

    response = requests.get(url, params=params, headers=headers)
    assert response.status_code == 200

    return response.json()


def filter_out_title_and_url(entries: dict, *, sort: bool = True) -> List[dict]:
    result = []
    for entry in entries["_embedded"]["items"]:
        result.append({"title": entry["title"], "url": entry["url"]})
    if sort:
        result = sorted(result, key=lambda x: x["title"])
    return result


def save_entries(
    entries: dict, *, file_path: str = "data/wallabag/entries.json", pretty: bool = True
):
    with open(file_path, "w") as f:
        if pretty:
            f.write(json.dumps(entries, indent=2, sort_keys=True))
        else:
            f.write(entries, sorted=True)


if __name__ == "__main__":
    token = get_bearer_token()
    entries = get_entries(token)
    title_and_url = filter_out_title_and_url(entries)
    save_entries(title_and_url)
