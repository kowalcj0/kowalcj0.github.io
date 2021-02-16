#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from typing import Dict, List, Optional

import tmdbsimple as tmdb
import wikipedia

wikipedia.set_lang("en")
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", None)
if TMDB_API_KEY:
    tmdb.API_KEY = TMDB_API_KEY
else:
    print("WARNING: TMDB_API_KEY env var is not set.")


def load_films(filename: str) -> List[str]:
    with open(filename) as f:
        films = json.load(f)
    return films


def page(query: str) -> Optional[wikipedia.wikipedia.WikipediaPage]:
    try:
        return wikipedia.page(query)
    except (
        wikipedia.exceptions.PageError,
        wikipedia.exceptions.DisambiguationError,
        wikipedia.exceptions.PageError,
    ):
        return None


def link(film_page: wikipedia.wikipedia.WikipediaPage, site: str) -> Optional[str]:
    matched = [r for r in film_page.references if site in r]
    return matched.pop() if matched else None


def get_tmdb_id(film: dict) -> Optional[int]:
    if not TMDB_API_KEY:
        return None
    tmdb_id = None
    if "tmdb" not in film and film["imdb"]:
        imdb_id = film["imdb"].split("/")[-2]
        response = tmdb.Find(imdb_id).info(external_source="imdb_id")
        if len(response["movie_results"]) == 1:
            movie = response["movie_results"][0]
            print(
                f"Found 1 match for IMDB title '{film['title']}' IMDB ID: {imdb_id} -> TMDB title '{movie['title']}' ID: {movie['id']}"
            )
            tmdb_id = movie["id"]
        elif len(response["movie_results"]) > 1:
            print(
                f"Found more than 1 match for IMDB title '{film['title']}' IMDB ID: {imdb_id}"
            )
            for movie in response["movie_results"]:
                print(f" -> TMDB title 'movie['title']' ID: {movie['id']}")
        else:
            print(
                f"IMDB title '{film['title']}' IMDB ID: {imdb_id} wasn't found in TMDB by IMDB ID"
            )
    return tmdb_id


def update(raw_films: dict) -> dict:
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
        tmdb_id = get_tmdb_id(film)
        if tmdb_id:
            raw_films["movies"][idx]["tmdb"] = tmdb_id

    return raw_films


def save(films):
    with open("new.json", "w") as write_file:
        json.dump(films, write_file, indent=4)


def main():
    films = load_films("data/movies/rezyseria_filmowa.json")
    updated = update(films)
    save(updated)


if __name__ == "__main__":
    main()
