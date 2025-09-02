import json
from utils import getDir


def read_json(path):
    """读取json文件"""
    try:
        path = f'{getDir.ROOT_DIR}/{path}'
        with open(path, 'r', encoding='utf-8') as f:
            api_data = json.load(f)
        return api_data
    except Exception as e:
        raise FileNotFoundError(e)


def read_file(path):
    """读取普通文件"""
    try:
        path = f'{getDir.ROOT_DIR}/{path}'
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise FileNotFoundError(e)
