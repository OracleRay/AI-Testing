import re
import json
import urllib.parse
import uuid
import copy

class IncompleteModelError(BaseException):
    pass

class Swagger:
    def __init__(self,source,deep=5):
        self.source = source
        self.deep = deep

        self.__scheme = self.schemes[0]
        servers = self.source.get('servers', [])
        if servers and len(servers) > 0 and 'url' in servers[0]:
            self.__host = servers[0]['url']
        else:
            self.__host = self.source.get('host') or 'localhost'

    def __property__(self,prop):
        if isinstance(prop, dict):
            _type = prop.get('type')
            _format = prop.get('format')
            _example = prop.get('example')
            if _example:
                prop = _example
            elif _type == 'integer':
                prop = 0
            elif _type == 'number':
                prop = 1.75
            elif _type == 'boolean':
                prop = True
            elif _type == 'string':
                if _format in [None,'byte', 'binary', 'password']:
                    prop = 'string'
                elif _format == 'date':
                    prop = '1970-01-01'
                elif _format == 'date-time':
                    prop = '1970-01-01 00:00:00'
            elif _type == 'file':
                prop = 'file.txt'
            elif _type == 'array':
                prop = []

        return prop

    @property
    def schemes(self):
        return self.source.get('schemes') or ['http']

    @property
    def scheme(self):
        return self.__scheme
    @scheme.setter
    def scheme(self,value):
        self.__scheme = value

    @property
    def host(self):
        return self.__host
    @host.setter
    def host(self,value):
        self.__host = value

    @property 
    def basePath(self):
        return self.source.get('basePath') or '/'

    @property    
    def models(self):
        ref_results = dict()

        definitions = copy.deepcopy(self.source.get('definitions'))
        for _ in range(self.deep):
            for key in list(definitions.keys()):
                properties = definitions[key].get('properties')
                if properties:
                    ref_keys = re.findall(r'"#/definitions/(.+?)"',json.dumps(properties,ensure_ascii=False))
                    if ref_keys and len(ref_keys)>0:
                        if set(ref_results.keys()).issuperset(set(ref_keys)):
                            for prop_name, prop in properties.items():
                                ref_key = prop.get('$ref')
                                if ref_key:
                                    properties[prop_name] = ref_results.get(ref_key.split('/').pop())
                                else:
                                    properties[prop_name] = self.__property__(prop)
                            ref_results.update({key: properties})
                            del definitions[key]
                    else:
                        for prop_name, prop in properties.items():
                            properties[prop_name] = self.__property__(prop)
                        ref_results.update({key: properties})
                        del definitions[key]
                else:
                    ref_results.update({key: dict()})
                    del definitions[key]
            # 无模型停止递归
            if len(definitions) == 0:
                break
        if len(definitions) > 0:
            raise IncompleteModelError('The model is incomplete. Please adjust the deep value of the swagger object.')
        return ref_results

    @property
    def apis(self):
        models = self.models

        api_results = []
    
        for path, forms in self.source.get('paths').items():
            for method, form in forms.items():
                name = form.get('summary')
                contentType = form.get('consumes') or ['']
                contentType = contentType[0]
            
                _path = (self.basePath+path).replace('//','/')
                url = urllib.parse.urlunparse((self.scheme, self.host, _path, None, None, None))
                _api = {
                    'id': uuid.uuid4().hex,
                    'name': name,
                    'method': method,
                    'path': _path,
                    'url': url,
                    'headers':{'Content-Type': contentType},
                    'paths':dict(),
                    'query':dict(),
                    'query_required':[],
                    'json':dict(),
                    'form':dict(),
                    'formData':dict()
                }
                # 参数提取
                parameters = form.get('parameters') or dict()
                for param in parameters:
                    _in = param.get('in')
                    paramName = param.get('name')
                    paramValue = self.__property__(param)

                    if isinstance(paramValue, dict):
                        schema = paramValue.get('schema')
                        if schema and schema.get('type') == 'array':
                            paramValue = []
                        else:
                            ref_key = re.search(r'"#/definitions/(.+?)"', json.dumps(schema, ensure_ascii=False))
                            if ref_key:
                                paramValue = models.get(ref_key.group(1))
                            else:
                                paramValue = self.__property__(schema) if schema else 'string'
                    if _in == 'header':
                        _api.get('headers').update({paramName: paramValue})
                    elif _in == 'path':
                        _api.get('paths').update({paramName: paramValue})
                    elif _in == 'query':
                        _api.get('query').update({paramName: paramValue})
                        # 提取required信息
                        if param.get('required'):
                            _api.get('query_required').append(paramName)
                    elif _in == 'body':
                        _api.update({'json':paramValue})
                    elif _in == 'formData':
                        if 'multipart/form-data' in contentType:
                            _api.get('formData').update({paramName: paramValue})
                        else:
                            _api.get('form').update({paramName: paramValue})
                
                # 处理 requestBody 字段
                request_body = form.get('requestBody') or dict()
                if request_body:
                    content = request_body.get('content') or dict()
                    json_content = content.get('application/json') or dict()
                    if json_content:
                        schema = json_content.get('schema') or dict()
                        if schema:
                            schema_value = self.__property__(schema)
                            if isinstance(schema_value, dict):
                                ref_key = re.search(r'"#/definitions/(.+?)"', json.dumps(schema, ensure_ascii=False))
                                if ref_key:
                                    schema_value = models.get(ref_key.group(1))
                                # else:
                                #     schema_value = self.__generate_schema(schema, models)
                            _api.update({'json': schema_value})
        
                api_results.append(_api)
        return api_results
