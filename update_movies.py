#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Movie Updater

Requirements:
    * python 3.6+
    * envparse https://pypi.org/project/envparse/
    * wikipedia https://pypi.org/project/wikipedia/
    * tmdbsimple https://pypi.org/project/tmdbsimple/

pip install envparse tmdbsimple wikipedia

This script also requires a .env, which is a simple KEY=VALUE file, e.g.:

TMDB_API_KEY=<some_key>

You can also provide those env vars in a regular way:

TMDB_API_KEY=<some_key> ./update_movies.py
"""
import argparse
import json
from typing import Optional

import tmdbsimple as tmdb
import wikipedia
from envparse import env
from scrapista.imdb import ImdbScraper

env.read_envfile()

WIKIPEDIA_LANG = env.str("WIKIPEDIA_LANG", default="en")
wikipedia.set_lang(WIKIPEDIA_LANG)

imdb_scraper = ImdbScraper()

TMDB_API_KEY = env.str("TMDB_API_KEY")
if TMDB_API_KEY:
    tmdb.API_KEY = TMDB_API_KEY
else:
    print("WARNING: TMDB_API_KEY env var is not set.")


def load_films(filename: str) -> dict:
    with open(filename) as input_file:
        films = json.load(input_file)
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
    if "imdb" not in film:
        return None
    if "tmdb" not in film and film["imdb"] and film["title"]:
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
    if "tmdb" in film and film["tmdb"]:
        tmdb_id = film["tmdb"]
    return tmdb_id



def update_ratings(movies: dict) -> dict:
    for idx, movie in enumerate(movies["movies"]):
        if movie["tmdb"]:
            print(f"Updating rating for: {movie['title']}")
            response = tmdb.Movies(movie["tmdb"])
            info = response.info()
            movie["rating_tmdb"] = info["vote_average"]
            movie["rating_tmdb_count"] = info["vote_count"]
            imdb_response = imdb_scraper.scrape_movie(movie["imdb"])
            movie["rating_imdb"] = imdb_response["rating_value"]
            movie["rating_imdb_count"] = imdb_response["rating_count"]
            movie["rating_imdb_metascore"] = imdb_response["metascore"] if imdb_response["metascore"] != "N/A" else None
            movie["rating_imdb_critic_count"] = imdb_response["critic_count"] if imdb_response["critic_count"] != "-" else None
    return movies


def find_film_pages_and_ids(raw_films: dict) -> dict:
    for idx, film in enumerate(raw_films["movies"]):
        if ("wiki" not in film or not film["wiki"]) and film["title"]:
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
                if "imdb" not in film or not film["imdb"]:
                    imdb = link(film_page, "imdb")
                    if imdb:
                        raw_films["movies"][idx]["imdb"] = imdb
                        print(f"Found imdb url: {imdb}")
                if "rt" not in film or not film["rt"]:
                    rotten = link(film_page, "rottentomatoes")
                    if rotten:
                        raw_films["movies"][idx]["rt"] = rotten
                        print(f"Found rottentomatoes url: {rotten}")
            else:
                print(f"Couldn't find {film['title']}")
        tmdb_id = get_tmdb_id(film)
        if tmdb_id:
            raw_films["movies"][idx]["tmdb"] = tmdb_id

    return raw_films


def save(films: dict, args: argparse.Namespace):
    output = args.input if args.in_place else args.output
    with open(output, "w") as write_file:
        json.dump(films, write_file, indent=4)


def main(args: argparse.Namespace):
    films = load_films(args.input)
    if args.rating:
        updated = update_ratings(films)
    else:
        updated = find_film_pages_and_ids(films)
    save(updated, args)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs=None, type=str, help="Input json movie file")
    parser.add_argument(
        "-i",
        "--in-place",
        action="store_true",
        help="Update input file in-place",
    )
    parser.add_argument(
        "--output",
        nargs=1,
        type=str,
        default="./updated.json",
        help="Output file (default: ./updated.json)",
    )
    parser.add_argument(
        "-r",
        "--rating",
        action="store_true",
        help="Only update external ratings",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = _parse_args()
    main(arguments)
