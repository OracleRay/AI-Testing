import json
import requests


def load_json(json_str):
    return json.loads(json_str)


def load_file(path):
    with open(path, encoding='utf8') as f:
        return load_json(f.read())


def load_url(url, method='get', **kwargs):
    return requests.request(url=url, method=method, **kwargs).json()