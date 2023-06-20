"""App to demo SWAPI Usage"""
from services.swapi import api as swapi
from utils import extract_film_urls, filter_ships_by_capacity


def main(min_capacity):
    ships = swapi.all_starships()
    filtered_ships = filter_ships_by_capacity(ships, min_capacity)
    film_urls = set(extract_film_urls(filtered_ships))
    return sorted(swapi.film_titles(film_urls))


if __name__ == '__main__':
    titles = main(1_000)
    print("=" * 50)
    for title in titles:
        print(title)