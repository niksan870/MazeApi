def construct_headers(token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["x-access-token"] = token
    return headers
