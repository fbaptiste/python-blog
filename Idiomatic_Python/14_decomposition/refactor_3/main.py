"""App to demo SWAPI Usage

Note: Technically SWAPI provides an SDK, but here my goal is to show
how to use decomposition to structure our code in a more readable, manageable,
and testable way.
"""
from services.swapi import api as swapi
from utils import extract_film_urls, filter_ships_by_capacity


def main(min_capacity):
    ships = swapi.all_starships()
    filtered_ships = filter_ships_by_capacity(ships, min_capacity)
    film_urls = set(extract_film_urls(filtered_ships))
    return swapi.film_titles(film_urls)


if __name__ == '__main__':
    titles = main(1_000)
    print("=" * 50)
    for title in titles:
        print(title)