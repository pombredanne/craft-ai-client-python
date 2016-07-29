def join_headers(old_headers, *new_headers):
    joined_headers = old_headers.copy()

    for header in new_headers:
        joined_headers.update(header)

    return joined_headers
