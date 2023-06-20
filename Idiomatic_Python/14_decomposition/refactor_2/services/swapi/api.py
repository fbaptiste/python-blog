"""SWAPI Service

Used for querying the SWAPI API.
"""
import requests
from requests.exceptions import Timeout, RequestException


BASE_URL = "https://swapi.dev/api"
MAX_ATTEMPTS = 5
INITIAL_TIMEOUT = 2  # seconds


def all_starships():
    """
    Retrieves a list of all starships from SWAPI.
    :return:
    """
    attempt_number = 1
    current_timeout = INITIAL_TIMEOUT
    ships = []
    request_url = f"{BASE_URL}/starships"

    while True:
        print(f"\trequesting: {request_url}")
        # max number of retries exceeded
        if attempt_number > MAX_ATTEMPTS:
            print("Exceeded max number of attempts")
            return

        # query API (with specific page)
        try:
            response = requests.get(
                request_url,
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

        # get JSON from response, and add ships from results to main ships list
        data = response.json()
        ships.extend(data.get("results", []))

        # is there a next page?
        if data.get('next'):
            request_url = data['next']
            # reset retry count and timeout (we start fresh for each page)
            current_timeout = INITIAL_TIMEOUT
            attempt_number = 1
        else:
            # done getting all results
            break

    return ships


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
                    print("Exceeded max number of attempts")
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