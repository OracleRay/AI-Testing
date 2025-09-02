import json
import os

from swaggers.swagger2 import swagger2
from utils.load_file import read_json


def get_apidoc(path):
    swagger = swagger2.parse_file(path)
    api_path = 'swaggers/api.json'
    if not os.path.exists(api_path):
        with open(api_path,mode='w',encoding='utf8') as f:
            f.write(json.dumps(swagger.apis,ensure_ascii=False))
    return read_json(api_path)