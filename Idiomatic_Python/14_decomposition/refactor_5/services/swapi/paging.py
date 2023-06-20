"""Utilities to implement api paging"""
def paged(single_page_func, initial_request_url):
    """
    Used to paginate API requests.

    :param single_page_func: a function that takes a single argument for the url to query
    :param initial_request_url: the initial starting page - this paging function will
        provide url for subsequent pages
    :return: a generator of results from all requested pages
    """
    next_request_url = initial_request_url
    while next_request_url:
        results, next_request_url = single_page_func(next_request_url)
        yield from results
