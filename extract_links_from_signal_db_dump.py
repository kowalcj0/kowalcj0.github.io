#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Requirements:
    * python 3.6+
    * envparse https://pypi.org/project/envparse/

pip install envparse

This script also requires a .env, which is a simple KEY=VALUE file, e.g.:

DB=signal_clear_text_messages_db_dump_filename.json
CONVO=00000000-1111-2222-3333-444444444444

You can also provide those env vars in a regular way:

DB=dbdump.json CONVO=00000000-1111-2222-3333-444444444444 ./extract_links_from_signal_db_dump.py
"""
import csv
import json
import re
from typing import List

from envparse import env

# read-in env vars from .env
env.read_envfile()

SIGNAL_CLEAR_TEXT_MESSAGES_DB_DUMP_FILENAME = env.str("DB")
CONVERSATION_ID = env.str("CONVO")


def get_db_entries() -> dict:
    with open(SIGNAL_CLEAR_TEXT_MESSAGES_DB_DUMP_FILENAME, "r") as f:
        return json.loads(f.read())


def get_messages_with_links(entries: dict) -> list:
    result = []
    for entry in entries:
        if "conversationId" in entry:
            if entry["conversationId"] == CONVERSATION_ID:
                if "body" in entry:
                    if entry["body"] is not None:
                        if "http" in entry["body"]:
                            result.append(entry["body"])
    return result


def chunks(lst: list, n: int):
    """Yield successive n-sized chunks from lst.
    SRC: https://stackoverflow.com/a/312464
    """
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def extract_urls_from_messages(messages: List[str]) -> List[str]:
    urls = []
    skip_words = [
        "youtu",
        "imdb.com",
        ".pl/",
        "vimeo",
        "twitter.com",
        "dictionary.com",
        ".jpg",
        "facebook.com",
        ".mp4",
    ]
    for msg in messages:
        url = re.search("(?P<url>https?://[^\s]+)", msg).group("url")
        if all(bar not in url for bar in skip_words):
            urls.append(url)
    return sorted(urls)


def save_urls_in_chunks(urls: List[str], *, prefix: str = "urls", chunk_size: int = 40):
    instapaper_csv_column_names = ["URL", "Title", "Selection", "Folder"]
    url_chunks = chunks(urls, chunk_size)
    for idx, chunk in enumerate(url_chunks):
        with open(f"{prefix}-{idx:03d}.csv", "w") as result_file:
            writer = csv.writer(result_file)
            writer.writerow(instapaper_csv_column_names)
            for url in chunk:
                row = [url, "", "", ""]
                writer.writerow(row)


if __name__ == "__main__":
    entries = get_db_entries()
    with_links = get_messages_with_links(entries)
    urls = extract_urls_from_messages(with_links)
    save_urls_in_chunks(urls)
