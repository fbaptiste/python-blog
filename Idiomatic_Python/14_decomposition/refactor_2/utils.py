"""Various utility functions used in SWAPI app"""

def films_for_min_capacity_ships(ships, min_capacity):
    """
    Determine films in which ships of a minimum capacity appear.

    :param ships: list of ship objects
    :param min_capacity: the minimum capacity (inclusive) of each ship
    :return: a list of film URLs
    """
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

    return list(film_urls)
