# Swagger2

#### 介绍
实现了Swagger文档生成Python请求数据功能，借助主流测试框架可快速完成大批量的接口测试任务。

#### 安装教程
```
pip install swagger2
```

#### 使用说明
* 快速开始
```python
'''文档转换'''
import json

import swagger2


url = 'https://petstore.swagger.io/v2/swagger.json'

swagger = swagger2.parse(url)

print('转换接口：{}个'.format(len(swagger.apis)))

api_path = 'api.json'
with open(api_path,mode='w',encoding='utf8') as f:
    f.write(json.dumps(swagger.apis,ensure_ascii=False))

'''api.json内容

[
    {
        "id": "de0993295bf94750980b3bf62e08a02b",
        "name": "uploadFile",
        "method": "post",
        "path": "/v2/pet/{petId}/uploadImage",
        "url": "https://petstore.swagger.io/v2/pet/{petId}/uploadImage",
        "headers": {
            "Content-Type": "multipart/form-data"
        },
        "paths": {
            "petId": 0
        },
        "query": {},
        "json": {},
        "form": {},
        "formData": {
            "additionalMetadata": "string",
            "file": "file.txt"
        }
    },
    {
        "id": "8b5d1baa6cc44e418861bc97c1a04855",
        "name": "addPet",
        "method": "post",
        "path": "/v2/pet",
        "url": "https://petstore.swagger.io/v2/pet",
        "headers": {
            "Content-Type": "application/json"
        },
        "paths": {},
        "query": {},
        "json": {
            "id": 0,
            "category": {
                "id": 0,
                "name": "string"
            },
            "name": "doggie",
            "photoUrls": [],
            "tags": [],
            "status": "string"
        },
        "form": {},
        "formData": {}
    },
    ...
    ...
]
'''
```
* 接口可用性测试
```python

import unittest
import requests
import os
import warnings

import swagger2

from swagger2 import utils


class APITestCase(unittest.TestCase):
    default_file = 'file.txt'

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore',ResourceWarning)
        # 准备测试资源
        if not os.path.exists(cls.default_file):
            with open(cls.default_file, mode='w') as f:
                f.write('Hello world!')

        url = 'https://petstore.swagger.io/v2/swagger.json'

        cls.swagger = swagger2.parse(url,verify=False)

    @classmethod
    def tearDownClass(cls):
        # 清理测试资源
        if os.path.exists(cls.default_file):
            os.remove(cls.default_file)

    def test_apis(self):
        for api in self.swagger.apis:
            with self.subTest(api.get('name')) as st:
                # 请求地址
                url = api.get('url')
                # 请求方法
                method = api.get('method')
                # 请求头
                headers = api.get('headers')
                # 路径参数
                paths = api.get('paths')
                # 查询字串，即query string
                params = api.get('query')
                # 普通表单，即 Content-Type = application/x-www-form-urlencoded
                data = api.get('form')
                # 文件表单, 即 Content-Type = multipart/form-data
                formData = api.get('formData')

                # json格式的参数, 即 Content-Type = application/json
                payload = api.get('json')

                # 文件上传时建议用requests框架的请求头
                if headers.get('Content-Type') == 'multipart/form-data':
                    del headers['Content-Type']
                # 路径参数格式化
                url = utils.path_format(url, paths)

                # 文件表单参数格式化
                formData = utils.form_format(formData)

                res = requests.request(method=method,
                                       url=url,
                                       headers=headers,
                                       params=params,
                                       data=data,
                                       files=formData,
                                       json=payload,
                                       timeout=30,
                                       verify=False)
                print(res.text)
                self.assertTrue(res.ok)


if __name__ == '__main__':
    unittest.main()
```


