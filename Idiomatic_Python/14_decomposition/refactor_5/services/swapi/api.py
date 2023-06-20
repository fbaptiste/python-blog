"""SWAPI Service

Used for querying the SWAPI API.
"""
import requests
from requests.exceptions import Timeout, RequestException

from services.swapi.paging import paged
from services.swapi.retries import timeout_retry


BASE_URL = "https://swapi.dev/api"
MAX_ATTEMPTS = 5
INITIAL_TIMEOUT = 1  # seconds



def starships(request_url, *, timeout=None):
    """
    Returns a single page's worth of starships

    :param request_url: the url to query
    :param timeout: timeout for request query
    :return: list of starships, and the URL for the next page (if any)
    """
    print(f"running query: {request_url}")

    retry_get = timeout_retry(max_attempts=MAX_ATTEMPTS, initial_timeout=INITIAL_TIMEOUT)(requests.get)
    response = retry_get(
        request_url,
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])
    next_page = data.get("next", None)

    return results, next_page


def all_starships():
    """
    Retrieves a list of all starships from SWAPI.
    :return: a generator of all starships
    """
    yield from paged(starships, f"{BASE_URL}/starships")


def film_title(film_url):
    """
    Gets title for a specific film
    :param film_url: url to query
    :return: a string title (or None if title is missing)
    """
    print(f"running query: {film_url}")

    retry_get = timeout_retry(max_attempts=MAX_ATTEMPTS, initial_timeout=INITIAL_TIMEOUT)(requests.get)
    response = retry_get(
        film_url,
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    data = response.json()
    return data.get("title")


def film_titles(film_urls):
    """
    Gets film titles for each film url passed to function
    :param film_urls: a list of film urls
    :return: a generator of titles
    """
    for film_url in film_urls:
        yield film_title(film_url)
