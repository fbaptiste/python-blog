"""SWAPI Service

Used for querying the SWAPI API.
"""
import requests
from requests.exceptions import Timeout, RequestException

from services.swapi.paging import paged


BASE_URL = "https://swapi.dev/api"
MAX_ATTEMPTS = 5
INITIAL_TIMEOUT = 2  # seconds


def starships(request_url):
    """
    Returns a single page's worth of starships

    :param request_url: the url to query
    :return: list of starships, and the URL for the next page (if any)
    """
    print(f"\trunning query: {request_url}")
    response = requests.get(
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



def film_titles(film_urls):
    results = set()
    for film_url in film_urls:
        attempt_number = 1
        current_timeout = INITIAL_TIMEOUT
        try:
            while True:
                print(f"\trequesting: {film_url}")
                # max number of retries exceeded
                if attempt_number > MAX_ATTEMPTS:
                    print("Exceed max number of attempts")
                    raise StopIteration  # we don't want to abort call, we'll just skip this film

                # query API
                try:
                    response = requests.get(
                        film_url,
                        headers={"Content-Type": "application/json"},
                        timeout=current_timeout
                    )
                    response.raise_for_status()
                except Timeout:
                    print("Request time out. Trying again with a longer timeout.")
                    current_timeout *= 2
                    attempt_number += 1
                    continue
                except RequestException as ex:
                    print(f"API query failed - aborting: {ex}")
                    return

                data = response.json()
                title = data.get("title")
                if title:
                    results.add(title)
                break
        except StopIteration:
            # inner loop wants to just move on to next film
            continue

    # return all film names as a sorted list
    return sorted(results)