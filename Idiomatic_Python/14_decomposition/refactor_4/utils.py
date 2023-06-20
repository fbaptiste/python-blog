"""Various utility functions used in SWAPI app"""

def filter_ships_by_capacity(ships, min_capacity):
    """
    Filters a list of ships based on some minimum capacity

    :param ships: list of ship objects
    :param min_capacity: the minimum capacity (inclusive) of each ship
    :return: a generator of ships
    """
    for ship in ships:
        try:
            cargo_capacity = int(ship["cargo_capacity"])
        except (KeyError, ValueError):
            # could not get a numeric cargo capacity, skip this ship
            continue
        if cargo_capacity >= min_capacity:
            yield ship


def extract_film_urls(ships):
    """
    For some iterable of ships, extracts the film URLs

    :param ships: list of ship objects
    :return: a generator (of potentially non-unique) film URLs
    """
    for ship in ships:
        if ship.get("films"):
            yield from ship["films"]
