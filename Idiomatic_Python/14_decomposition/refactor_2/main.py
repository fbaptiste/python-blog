"""App to demo SWAPI Usage

Note: Technically SWAPI provides an SDK, but here my goal is to show
how to use decomposition to structure our code in a more readable, manageable,
and testable way.
"""
from services.swapi import api as swapi
from utils import films_for_min_capacity_ships


def main(min_capacity: int):
    ships = swapi.all_starships()
    film_urls = films_for_min_capacity_ships(ships, min_capacity)
    return swapi.film_titles(list(film_urls))


if __name__ == '__main__':
    titles = main(1_000)
    print("=" * 50)
    for title in titles:
        print(title)