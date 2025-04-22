from urllib.parse import urlparse, parse_qs


def parse_url_to_json(input) -> dict:
    if not isinstance(input, str):
        raise TypeError(f'Input should be a string, found {type(input)}')
    
    parsed_url = urlparse(input)
    
    return {
        "scheme": parsed_url.scheme,
        "netloc": parsed_url.netloc,
        "path": parsed_url.path,
        "params": parsed_url.params,
        "query": parse_qs(parsed_url.query),
        "fragment": parsed_url.fragment,
        "username": parsed_url.username,
        "password": parsed_url.password,
        "hostname": parsed_url.hostname,
        "port": parsed_url.port,
    }
