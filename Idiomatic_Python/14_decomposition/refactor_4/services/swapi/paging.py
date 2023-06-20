"""Utilities to implement api paging"""
def paged(single_page_func, initial_request_url):
    next_request_url = initial_request_url
    while next_request_url:
        results, next_request_url = single_page_func(next_request_url)
        yield from results
