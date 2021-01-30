#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from typing import Dict, List, Optional

import wikipedia

wikipedia.set_lang("en")


def load_films(filename: str) -> List[str]:
    with open(filename) as f:
        films = json.load(f)
    return films


def page(query: str) -> Optional[wikipedia.wikipedia.WikipediaPage]:
    try:
        return wikipedia.page(query)
    except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
        return None


def link(film_page: wikipedia.wikipedia.WikipediaPage, site: str) -> Optional[str]:
    matched = [r for r in film_page.references if site in r]
    return matched.pop() if matched else None


def update(raw_films: dict) -> List[wikipedia.wikipedia.WikipediaPage]:
    for idx, film in enumerate(raw_films["movies"]): 
        if not film["wiki"]:
            query = f"{film['title']} (film)"
            print(f"Searching for: {query}")
            film_page = page(query)
            if not film_page:
                query = f"{film['title']} (film) {film['year']}"
                print(f"Searching for: {query}")
                film_page = page(query)
            if not film_page:
                query = f"{film['title']} {film['year']}"
                print(f"Searching for: {query}")
                film_page = page(query)
            if not film_page:
                query = f"{film['title']}"
                print(f"Searching for: {query}")
                film_page = page(query)
            if film_page:
                print(f"Found page for: {film['title']}")
                raw_films["movies"][idx]["wiki"] = film_page.url
                if not film["imdb"]:
                    imdb = link(film_page, "imdb")
                    if imdb:
                        raw_films["movies"][idx]["imdb"] = imdb
                        print(f"Found imdb url: {imdb}")
                if not film["rt"]:
                    rt = link(film_page, "rottentomatoes")
                    if rt:
                        raw_films["movies"][idx]["rt"] = rt
                        print(f"Found rottentomatoes url: {rt}")
            else:
                print(f"Couldn't find {film['title']}")
    return raw_films


def save(films):
    with open("new.json", "w") as write_file:
        json.dump(films, write_file, indent=4)


def main():
    films = load_films("rezyseria_filmowa.json")
    updated = update(films)
    save(updated)

