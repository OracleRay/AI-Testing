import string
import re


def path_format(url,params):
    t = string.Template(re.subn(r'{(\w+)}',r'${\1}',url)[0])
    return t.safe_substitute(params)

def form_format(data:dict):
    _data = dict()
    for k,v in data.items():
        if v == 'file.txt':
            v = (k,open('file.txt',mode='rb'))
        else:
            v = (None,v)
        _data.update({k:v})

    return _data