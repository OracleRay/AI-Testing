import json
import random
import datetime
import urllib3
from loguru import logger
from urllib.parse import urlparse, urlencode
import os
from dotenv import find_dotenv, load_dotenv
from faker import Faker
from configs.config import ConfigManager
from utils import log

log.Logging()

_, plat_config = ConfigManager.get_openplatform('open_new')


# 开放平台请求钩子
def hooks_open_request(request, token=True, sig=False):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    load_dotenv(find_dotenv())
    params = {}
    param_type = ""
    if request['req_json']:
        params = request['req_json']
        param_type = 'req_json'
    elif request['params']:
        params = request['params']
        param_type = 'params'
    elif request['data']:
        params = request['data']
        param_type = 'data'
    else:
        logger.info("请求无参数")
        pass
    payload = {}
    if params:
        for k, v in params.items():
            if v is not None:
                payload[k] = v
        request[param_type] = payload
    if token:
        request['headers']['Authorization'] = os.environ.get("access_token")
    if not token and sig:
        if param_type == 'req_json':
            sig_url = urlparse(request['url']).path
            body = json.dumps(payload)
        else:
            sig_url = f"{urlparse(request['url']).path}?{urlencode(payload)}"
            body = ''
        sign_params = {
            "method": request["method"],
            "url": sig_url,
            "body": body,
            "key": plat_config["platform_key"]
        }
        logger.info(f"signature body {sign_params}")
        from utils import sign_utils
        sign = sign_utils.gen_sign(sign_params)
        request['headers']['platformcode'] = plat_config["platform_key"]
        request['headers']['Platform-Sign'] = sign


# 开放平台返回解密
def hooks_open_response(response, key="aes_key"):
    load_dotenv(find_dotenv())
    assert response.status_code == 200
    body = response.body
    if body.get("code") == 0 and key:
        aes_key = plat_config['aes_key']
        from utils import aes_utils
        decode_data = aes_utils.aes_cryption(type='decode', data=body['encrypt'], AES_KEY=aes_key)
        logger.info(f"-----------------aes decode data {decode_data}")
        response.body = decode_data


# 获取返回值中的对应key的value
def response_data(response, key=None, index=0):
    if isinstance(response, dict) and key:
        return response.get(key)
    elif isinstance(response, list) and key:
        return response[index].get(key)
    else:
        return response


def count_addition(a, b) -> int:
    return int(a) + int(b)


Fake = Faker("zh_CN")


def gen_address():
    """
    生成随机地址
    :return:
    """
    return Fake.address()


def gen_phone():
    """
    生成随机手机号
    :return:
    """
    return Fake.phone_number()


def Generate_random_string():  # 生成6位随机字符串
    a = ''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
         'd', 'c', 'b', 'a'], 6))
    return a


# 生成小数位后16位的随机数
def get_random_16():
    for i in range(100):
        a = str(random.random())
        if len(a) == '18':
            break
        return a
    return None


def gen_name():
    """
    生成随机人名
    :return:
    """
    return Fake.name()


def gen_com_name():
    """
    生成随机公司名
    :return:
    """
    return Fake.company()


def gen_job():
    """
    生成职位
    :return:
    """
    return Fake.job()


def gen_email():
    """
    生成电子邮箱
    :return:
    """
    return Fake.email()


# 输入相对当天的差值天数.获取指定日期
def get_date(delta):
    # 获得当前时间
    d1 = datetime.datetime.now()
    # 转换为指定的格式
    d3 = d1 + datetime.timedelta(days=delta)
    otherStyleTime = d3.strftime("%Y-%m-%d")
    print(otherStyleTime)
    return otherStyleTime