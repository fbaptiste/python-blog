"""SWAPI Demo

Note: Technically SWAPI provides an SDK, but here my goal is to show
how to use decomposition to structure our code in a more readable, manageable,
and testable way.
"""

from services.swapi import api as swapi

def main(min_capacity: int):
    # get all ships
    ships = swapi.all_starships()

    # filter the ones we want, and just store the film urls
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

    # retrieve and return all the film titles
    return swapi.film_titles(film_urls)


if __name__ == '__main__':
    titles = main(1_000)
    print("=" * 50)
    for title in titles:
        print(title)