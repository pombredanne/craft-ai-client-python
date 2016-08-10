from craftai.errors import *


def join_headers(old_headers, *new_headers):
    joined_headers = old_headers.copy()

    for header in new_headers:
        joined_headers.update(header)

    return joined_headers


def dict_depth(x):
    if type(x) is dict and x:
        return 1 + max(dict_depth(x[a]) for a in x)
    if type(x) is list and x:
        return 1 + max(dict_depth(a) for a in x)
    return 0
