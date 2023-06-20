"""SW API Demo

A perfect example of how NOT to write code.
"""
import requests
from requests.exceptions import Timeout, RequestException


def starship_films(min_capacity):
    # query API, with retry if timeout happens, up to some max number of times
    attempt_number = 1
    max_attempts = 5
    initial_timeout = 1
    current_timeout = initial_timeout
    ships = []  # holds collection of all ships retried from paging API
    request_url = "https://swapi.dev/api/starships"  # default to first page
    while True:
        print(f"\trequesting: {request_url}")
        # max number of retries exceeded
        if attempt_number > max_attempts:
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
            current_timeout = initial_timeout
            attempt_number = 1
        else:
            # done getting all results
            break

    # find all ships with a minimum cargo capacity
    film_urls = set()
    for ship in ships:
        try:
            cargo_capacity = int(ship["cargo_capacity"])
        except (KeyError, ValueError):
            # could not get a numeric cargo capacity, skip this ship
            continue
        if cargo_capacity >= min_capacity:
            if ship.get("films"):
                film_urls.update(ship["films"])

    # Collect film titles for each film identified (paging not needed, but want timeout retries)
    film_titles = set()
    for film_url in film_urls:
        attempt_number = 1
        initial_timeout = 2
        current_timeout = initial_timeout
        try:
            while True:
                print(f"\trequesting: {film_url}")
                # max number of retries exceeded
                if attempt_number > max_attempts:
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
                    film_titles.add(title)
                break
        except StopIteration:
            # inner loop wants to just move on to next film
            continue

    # return all film names as a sorted list
    return sorted(film_titles)


if __name__ == '__main__':
    films = starship_films(1_000)
    print("=" * 50)
    for film in films:
        print(film)