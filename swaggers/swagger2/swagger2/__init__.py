from .loader import *
from .swagger import *

def parse(url,deep=5,**kwargs):
    source = load_url(url,**kwargs)
    return Swagger(source,deep=deep)

def parse_file(path,deep=5):
    source = load_file(path)
    return Swagger(source,deep=deep)

