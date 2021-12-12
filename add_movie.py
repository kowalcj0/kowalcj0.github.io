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
from enum import Enum
from pathlib import Path
from pprint import pprint
from typing import List, Optional, Tuple
from urllib.parse import urljoin

import tmdbsimple as tmdb
import wikipedia
from envparse import env
from justwatch import JustWatch
from rotten_tomatoes_client import RottenTomatoesClient


class SearchFor(Enum):
    MOVIE = "movie"
    TV = "TV"


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


def  set_what_are_you_looking_for() -> SearchFor:
    """Define watch date."""
    decision = input(
        f"Did you watch a movie or a TV show? for a movie -> [y/m/Enter]; for a TV -> [t/tv/n]?: "
    ).lower()
    if decision in ["y", "m", ""]:
        search_for = SearchFor.MOVIE
    elif decision in ["n", "t", "tv"]:
        search_for = SearchFor.TV
    else:
        raise TypeError(f"Invalid type of saught show: {what}")
    return search_for


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


def set_rating_my() -> str:
    """Define my rating."""
    decision = input(f"What's the movie score on a scale from 0 to 3?: ").lower()
    return int(decision)


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


def load_tv_shows() -> dict:
    file_path = Path(f"./data/movies/tv_shows.json")
    if file_path.is_file():
        with open(file_path) as input_file:
            shows = json.load(input_file)
    else:
        shows = {
            "category": "tv_shows",
            "movies": [],
        }
    return shows


def page(query: str) -> Optional[wikipedia.wikipedia.WikipediaPage]:
    try:
        return wikipedia.page(query)
    except (
        wikipedia.exceptions.PageError,
        wikipedia.exceptions.DisambiguationError,
        wikipedia.exceptions.PageError,
    ):
        return None


def find_wiki_page_url(title: str, year: int, *, tv_show: bool = False) -> Optional[str]:
    if not tv_show:
        suffix = "Film"
    else:
        suffix = "TV series"
    query = f"{title} ({suffix})"
    print(f"Wiki: Searching for: {query}")
    film_page = page(query)
    if not film_page:
        query = f"{title} ({suffix}) {year}"
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


def add_tv_show_details(show: dict) -> dict:
    shows = load_tv_shows()
    shows["movies"].append(show)
    return shows


def save(contents: dict, category: str):
    output = f"./data/movies/{category}.json"
    with open(output, "w") as write_file:
        json.dump(contents, write_file, indent=4)


def search_tmdb_for_tv_show(title: str) -> dict:
    """
    An example TV show search results:
    [
        {
            "backdrop_path":"/b6vueHvnoArdRbZKlxZR7o4BVWU.jpg",
            "first_air_date":"2018-10-27",
            "genre_ids":[
                80
            ],
            "id":82858,
            "name":"Blinded by the Lights",
            "origin_country":[
                "PL"
            ],
            "original_language":"pl",
            "original_name":"Ślepnąc od świateł",
            "overview":"An eight-episode story charting seven days from the life of a cocaine dealer whose perfectly organized life begins to sink into chaos while he is forced to make the most important choices in his life.",
            "popularity":4.949,
            "poster_path":"/gXCa394XSso2QNgxxxIIn9zScj8.jpg",
            "vote_average":7.3,
            "vote_count":12
        }
    ]
    """
    search = tmdb.Search()
    response = search.tv(query=title)
    results = response["results"]
    show = None
    if len(results) == 1:
        show = results[0]
        print(
            f"Found 1 match for title '{title}' -> TMDB title '{show['name']}' {show['first_air_date']} ID: {show['id']}"
        )
    elif len(results) > 1:
        print(f"Found {len(results)} matching titles in TMDB")
        for idx, result in enumerate(results):
            print(
                f"{idx:2} -> {result['name']} (orig. {result['original_name']}) {result['first_air_date']} ID: {result['id']}"
            )
        number = None
        while number not in range(len(results)):
            value = input(
                f"Pick the show number from 0 to {len(results)-1} or q to quit: "
            )
            if value.isdigit():
                number = int(value)
            if value.lower() == "q":
                sys.exit()
        show = results[number]
    else:
        print(f"No show was found in TMDB using title: {title}")
        sys.exit()
    return tmdb.TV(id=show["id"])



def search_tmdb_for_movie(title: str) -> dict:
    search = tmdb.Search()
    response = search.movie(query=title)
    results = response["results"]
    movie = None
    if len(results) == 1:
        movie = results[0]
        print(
            f"Found 1 match for title '{title}' -> TMDB title '{movie['title']}' {movie['release_date']} ID: {movie['id']}"
        )
    elif len(results) > 1:
        print(f"Found {len(results)} matching titles in TMDB")
        for idx, result in enumerate(results):
            print(
                f"{idx:2} -> {result['title']} (orig. {result['original_title']}) {result['release_date']} ID: {result['id']}"
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
        for score in movie.get("scoring", []):
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


def filter_movie_details(movie: tmdb.movies.Movies, watched_date: str) -> dict:
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


def filter_tv_show_details(show: tmdb.tv.TV, watched_date: str) -> dict:
    """Filter out unwanted details."""
    info = show.info()
    directors = [person["name"] for person in info["created_by"]]
    videos = show.videos()
    """
    INFO:
    {
        "backdrop_path":"/b6vueHvnoArdRbZKlxZR7o4BVWU.jpg",
        "created_by":[
            {
                "id":481162,
                "credit_id":"5bb74d8c9251410dd102685a",
                "name":"Krzysztof Skonieczny",
                "gender":0,
                "profile_path":"None"
            },
            {
                "id":1688994,
                "credit_id":"5bb74d990e0a263393024f77",
                "name":"Jakub Żulczyk",
                "gender":0,
                "profile_path":"None"
            }
        ],
        "episode_run_time":[
            55
        ],
        "first_air_date":"2018-10-27",
        "genres":[
            {
                "id":80,
                "name":"Crime"
            }
        ],
        "homepage":"https://www.hbo.pl/series/slepnac-od-swiatel",
        "id":82858,
        "in_production":false,
        "languages":[
            "pl"
        ],
        "last_air_date":"2018-10-27",
        "last_episode_to_air":{
            "air_date":"2018-10-27",
            "episode_number":8,
            "id":1599567,
            "name":"",
            "overview":"Kuba is getting ready to leave Poland. It's early morning and the plane departs in the evening. Will he manage to fix things before he leaves?",
            "production_code":"",
            "season_number":1,
            "still_path":"/m5p6NaHJ7YtJtW3eKjvp5nv87bV.jpg",
            "vote_average":0.0,
            "vote_count":0
        },
        "name":"Blinded by the Lights",
        "next_episode_to_air":"None",
        "networks":[
            {
                "name":"HBO Europe",
                "id":1129,
                "logo_path":"/tyoN6zoxMJ71GBddxVkk4dpaeze.png",
                "origin_country":""
            }
        ],
        "number_of_episodes":8,
        "number_of_seasons":1,
        "origin_country":[
            "PL"
        ],
        "original_language":"pl",
        "original_name":"Ślepnąc od świateł",
        "overview":"An eight-episode story charting seven days from the life of a cocaine dealer whose perfectly organized life begins to sink into chaos while he is forced to make the most important choices in his life.",
        "popularity":4.949,
        "poster_path":"/gXCa394XSso2QNgxxxIIn9zScj8.jpg",
        "production_companies":[
            {
                "id":75269,
                "logo_path":"None",
                "name":"House Media Company",
                "origin_country":"PL"
            }
        ],
        "production_countries":[
            {
                "iso_3166_1":"PL",
                "name":"Poland"
            }
        ],
        "seasons":[
            {
                "air_date":"2018-10-27",
                "episode_count":8,
                "id":110352,
                "name":"Season 1",
                "overview":"",
                "poster_path":"/aBryHTDFDhNOH3sv3huG2aPWajQ.jpg",
                "season_number":1
            }
        ],
        "spoken_languages":[
            {
                "english_name":"Polish",
                "iso_639_1":"pl",
                "name":"Polski"
            }
        ],
        "status":"Ended",
        "tagline":"",
        "type":"Miniseries",
        "vote_average":7.3,
        "vote_count":12
    }

    VIDEOS:
    {
        "id":82858,
        "results":[
            {
                "id":"5bcbc341c3a368239d008f71",
                "iso_639_1":"en",
                "iso_3166_1":"US",
                "key":"4vXasjfxye4",
                "name":"Blinded By The Lights - trailer",
                "site":"YouTube",
                "size":1080,
                "type":"Trailer"
            }
        ]
    }
    """
    yt_trailers = [
        v["key"]
        for v in videos["results"]
        if v["site"] == "YouTube" and v["type"] == "Trailer"
    ]
    if yt_trailers:
        trailer = f"https://www.youtube.com/watch?v={yt_trailers[0]}"
    else:
        trailer = ""
    year = int(info["first_air_date"].split("-")[0])

    wiki = find_wiki_page_url(info["name"], year, tv_show=True)

    just_watch_url, netflix_url = search_just_watch(info["name"], info["id"])
    rotten_tomatoes_url = search_rotten_tomatoes(info["name"])
    result = {
        "title": info["name"],
        "original_title": info["original_name"]
        if info["original_name"] != info["name"]
        else "",
        "director": ", ".join(directors) if len(directors) > 1 else directors[0],
        "genres": [genre["name"].lower() for genre in info["genres"]],
        "year": year,
        "trailer": trailer,
        "wiki": wiki or "",
        "imdb": f"https://www.imdb.com/title/{info['imdb_id']}/" if "imdb_id" in info else "",
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
        3. add my rating
        4. pick movie category
        5. add movie to category
        6. save movie category
    """
    search_for = set_what_are_you_looking_for()
    watched_date = set_watched_date()
    rating_my = set_rating_my()
    if search_for == SearchFor.MOVIE:
        tmdb_movie = search_tmdb_for_movie(title)
        details = filter_movie_details(tmdb_movie, watched_date)
        details["rating_my"] = rating_my
        category = pick_category()
        updated = add_movie_to_category(details, category)
    elif search_for == SearchFor.TV:
        tmdb_movie = search_tmdb_for_tv_show(title)
        details = filter_tv_show_details(tmdb_movie, watched_date)
        category = "tv_shows"
        details["rating_my"] = rating_my
        updated = add_tv_show_details(details)
    save(updated, category)


if __name__ == "__main__":
    check_env()
    main(title=parse_args())
