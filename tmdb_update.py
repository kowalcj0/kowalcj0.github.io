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

import requests
import tmdbsimple as tmdb
import wikipedia
from envparse import env

env.read_envfile()

TMDB_API_KEY = env.str("TMDB_API_KEY")
if TMDB_API_KEY:
    tmdb.API_KEY = TMDB_API_KEY
else:
    print("WARNING: TMDB_API_KEY env var is not set.")


def load_films(filename: str) -> dict:
    with open(filename) as input_file:
        films = json.load(input_file)
    return films


def update(raw_films: dict) -> dict:
    for idx, film in enumerate(raw_films["movies"]):
        if "tmdb" in film and film["tmdb"]:
            try:
                movie = tmdb.Movies(film["tmdb"])
                info = movie.info()
                if info["production_countries"]:
                    raw_films["movies"][idx]["production_countries"] = info["production_countries"]
                else:
                    print(f"No production countries for {film['title']}")

                crew = movie.credits()["crew"]
                directors = [person["name"] for person in crew if person["job"] == "Director"]
                if directors:
                    raw_films["movies"][idx]["director"] = ", ".join(directors) if len(directors) > 1 else directors[0]
                else:
                    print(f"No director found for {film['title']}")

                videos = movie.videos()
                yt_trailers = [
                    v["key"]
                    for v in videos["results"]
                    if v["site"] == "YouTube" and v["type"] == "Trailer"
                ]
                if yt_trailers:
                    trailer = f"https://www.youtube.com/watch?v={yt_trailers[0]}"
                    raw_films["movies"][idx]["trailer"] = trailer
            except requests.exceptions.HTTPError:
                    print(f"Movie not found {film['title']}")
    return raw_films


def save(films: dict, args: argparse.Namespace):
    output = args.input if args.in_place else args.output
    with open(output, "w") as write_file:
        json.dump(films, write_file, indent=4)


def main(args: argparse.Namespace):
    films = load_films(args.input)
    updated = update(films)
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
    return parser.parse_args()


if __name__ == "__main__":
    arguments = _parse_args()
    main(arguments)
