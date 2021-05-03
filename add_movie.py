#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Movie Finder

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
import os
import sys
from datetime import date
from pathlib import Path
from pprint import pprint
from typing import List, Optional, Tuple
from urllib.parse import urljoin

import tmdbsimple as tmdb
import wikipedia
from envparse import env
from justwatch import JustWatch
from rotten_tomatoes_client import RottenTomatoesClient


def parse_args() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("title", nargs="*", type=str, help="Movie title")
    args = parser.parse_args()
    return " ".join(args.title)


def check_env():
    env.read_envfile()

    wikipedia.set_lang(env.str("WIKIPEDIA_LANG", default="en"))

    if tmdb_api_key := env.str("TMDB_API_KEY"):
        tmdb.API_KEY = tmdb_api_key
    else:
        sys.exit("TMDB_API_KEY env var is not set")


def set_watched_date() -> str:
    """Define watch date."""
    today = date.today().strftime("%Y-%m-%d")
    decision = input(
        f"When did you watch it? Perhaps today {today} [y/Enter]?: "
    ).lower()
    if decision in ["y", ""]:
        watch_date = today
    else:
        watch_date = decision
    return watch_date


def find_categories() -> List[str]:
    """Find movie categories"""
    categories = []
    for _, _, files in os.walk("./data/movies"):
        for filename in files:
            extension = Path(filename).suffix
            stem = Path(filename).stem
            if extension.lower() == ".json":
                categories.append(stem)
    return categories


def load_movie_category(category: str) -> dict:
    file_path = Path(f"./data/movies/{category}.json")
    if file_path.is_file():
        with open(file_path) as input_file:
            movies = json.load(input_file)
    else:
        movies = {
            "category": category,
            "movies": [],
        }
    return movies


def page(query: str) -> Optional[wikipedia.wikipedia.WikipediaPage]:
    try:
        return wikipedia.page(query)
    except (
        wikipedia.exceptions.PageError,
        wikipedia.exceptions.DisambiguationError,
        wikipedia.exceptions.PageError,
    ):
        return None


def find_wiki_page_url(title: str, year: int) -> Optional[str]:
    query = f"{title} (film)"
    print(f"Wiki: Searching for: {query}")
    film_page = page(query)
    if not film_page:
        query = f"{title} (film) {year}"
        print(f"Searching for: {query}")
        film_page = page(query)
    if not film_page:
        query = f"{title} {year}"
        print(f"Searching for: {query}")
        film_page = page(query)
    if not film_page:
        query = f"{title}"
        print(f"Searching for: {query}")
        film_page = page(query)
    url = None
    if film_page:
        print(f"Wiki: Found page for: {title}")
        url = film_page.url
    else:
        print(f"Wiki: Couldn't find {title}")
    return url


def add_movie_to_category(movie: dict, category: str) -> dict:
    movies = load_movie_category(category)
    movies["movies"].append(movie)
    return movies


def save(films: dict, category: str):
    output = f"./data/movies/{category}.json"
    with open(output, "w") as write_file:
        json.dump(films, write_file, indent=4)


def search_tmdb(title: str) -> dict:
    search = tmdb.Search()
    response = search.movie(query=title)
    results = response["results"]
    movie = None
    if len(results) == 1:
        movie = results[0]
        print(
            f"Found 1 match for title '{title}' -> TMDB title '{movie['title']}' ID: {movie['id']}"
        )
    elif len(results) > 1:
        print(f"Found {len(results)} matching titles in TMDB")
        for idx, result in enumerate(results):
            print(
                f"{idx:2} -> {result['title']} (orig. {result['original_title']}) ID: {result['id']}"
            )
        number = None
        while number not in range(len(results)):
            value = input(
                f"Pick the movie number from 0 to {len(results)-1} or q to quit: "
            )
            if value.isdigit():
                number = int(value)
            if value.lower() == "q":
                sys.exit()
        movie = results[number]
    else:
        print(f"No movie was found in TMDB using title: {title}")
        sys.exit()
    return tmdb.Movies(movie["id"])


def search_just_watch(
    title: str, tmdb_id: int, year: int = None
) -> Tuple[Optional[str], Optional[str]]:
    """Search justwatch by title and TMBD ID."""

    def look_for_netflix_url(movie: dict) -> Optional[str]:
        netflix_provider_id = 8
        for offer in movie.get("offers"):
            if offer.get("provider_id") == netflix_provider_id:
                print(
                    f"Found '{movie['title']}' on Netflix {offer['urls']['standard_web']}"
                )
                return offer["urls"]["standard_web"]
        return None

    just_watch_domanin = "https://www.justwatch.com"
    just_watch = JustWatch(country="GB")
    results = just_watch.search_for_item(
        query=title, release_year_from=year, page_size=100
    )
    for movie in results["items"]:
        for score in movie.get("scoring"):
            if score.get("provider_type") == "tmdb:id":
                if score.get("value") == tmdb_id:
                    print(f"Found '{title}' on JustWatch.com by tmdb id: {tmdb_id}")
                    just_watch_url = urljoin(just_watch_domanin, movie["full_path"])
                    netflix_url = look_for_netflix_url(movie)
                    return just_watch_url, netflix_url

    ascii_title = "".join(c for c in title.lower() if c.isalnum())
    for movie in results["items"]:
        ascii_result_title = "".join(c for c in movie["title"].lower() if c.isalnum())
        if ascii_title == ascii_result_title:
            print(f"Found '{title}' on JustWatch.com by an exact title match")
            just_watch_url = urljoin(just_watch_domanin, movie["full_path"])
            netflix_url = look_for_netflix_url(movie)
            return just_watch_url, netflix_url
    print(f"Could not find '{title}' on JustWatch.com by title and tmdb id")
    return None, None


def search_rotten_tomatoes(title: str) -> Optional[str]:
    """Search Rotten Tomatoes Public API by title."""
    rotten_tomatoes_domanin = "https://www.rottentomatoes.com/"
    results = RottenTomatoesClient.search(term=title, limit=5)
    ascii_title = "".join(c for c in title.lower() if c.isalnum())
    for movie in results["movies"]:
        ascii_result_title = "".join(c for c in movie["name"].lower() if c.isalnum())
        if ascii_title == ascii_result_title:
            print(f"Found '{title}' on rottentomatoes.com by an exact title match")
            url = urljoin(rotten_tomatoes_domanin, movie["url"])
            return url
    print(f"Could not find '{title}' on rottentomatoes.com by title")
    return None


def pick_category() -> str:
    categories = find_categories()
    print(
        f"Pick category number from 0 to {len(categories)-1} or q to quit, n for new: "
    )
    for idx, category in enumerate(categories):
        print(f"{idx:2} -> {category}")
    number = None
    new_category = None
    while number not in range(len(categories)):
        value = input()
        if value.isdigit():
            number = int(value)
        if value.lower() == "n":
            new_category = input("Enter new category name: ")
            break
        if value.lower() == "q":
            sys.exit()
    if new_category:
        return new_category
    return categories[number]


def filter_details(movie: tmdb.movies.Movies, watched_date: str) -> dict:
    """Filter out unwanted details."""
    info = movie.info()
    crew = movie.credits()["crew"]
    videos = movie.videos()
    directors = [person["name"] for person in crew if person["job"] == "Director"]
    yt_trailers = [
        v["key"]
        for v in videos["results"]
        if v["site"] == "YouTube" and v["type"] == "Trailer"
    ]
    if yt_trailers:
        trailer = f"https://www.youtube.com/watch?v={yt_trailers[0]}"
    else:
        trailer = ""
    year = int(info["release_date"].split("-")[0])

    wiki = find_wiki_page_url(info["title"], year)

    just_watch_url, netflix_url = search_just_watch(info["title"], info["id"])
    rotten_tomatoes_url = search_rotten_tomatoes(info["title"])

    result = {
        "title": info["title"],
        "original_title": info["original_title"]
        if info["original_title"] != info["title"]
        else "",
        "director": ", ".join(directors) if len(directors) > 1 else directors[0],
        "genres": [genre["name"].lower() for genre in info["genres"]],
        "year": year,
        "trailer": trailer,
        "wiki": wiki or "",
        "imdb": f"https://www.imdb.com/title/{info['imdb_id']}/",
        "rt": rotten_tomatoes_url or "",
        "netflix": netflix_url or "",
        "justwatch": just_watch_url or "",
        "comments": "",
        "tmdb": info["id"],
        "watched": watched_date,
        "production_countries": info["production_countries"],
    }
    pprint(result)
    return result


def main(title: str):
    """Find movie details and save them.
    Steps:
        1. look for movie details
        2. filter out redundant details
        3. pick movie category
        4. add movie to category
        5. save movie category
    """
    watched_date = set_watched_date()
    tmdb_movie = search_tmdb(title)
    movie = filter_details(tmdb_movie, watched_date)
    category = pick_category()
    updated = add_movie_to_category(movie, category)
    save(updated, category)


if __name__ == "__main__":
    check_env()
    main(title=parse_args())
