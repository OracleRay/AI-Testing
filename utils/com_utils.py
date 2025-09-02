#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import random
import arrow
from faker import Factory
import os
import time, hashlib
from utils.get_directory import PROJECT_DIR
from loguru import logger

"""
创建测试数据方法
"""
f = Factory().create('zh-CN')
with open(f"{PROJECT_DIR}/utils/city_info/city", "r", encoding='utf-8') as city:
    city_info = eval(city.read())

with open(f"{PROJECT_DIR}/utils/city_info/record", "r", encoding='utf-8') as city:
    record = city.readlines()


# 按ascall码排序拼接参数
def sort_param(params):
    result = ''
    length = len(params)
    num = 1
    for i in sorted(params):
        if num == length:
            result += str(params[i])
        else:
            result += str(params[i]) + ';'
        num += 1
    # print(result)
    return result


def mkdir(dir_path):
    """ 创建路径
    """
    # 去除首位空格
    _dir = dir_path.strip()
    _dir = dir_path.rstrip("\\")
    _dir = dir_path.rstrip("/")

    # 判断路径是否存在
    is_exists = os.path.exists(_dir)

    if not is_exists:
        try:
            os.makedirs(_dir)
        except Exception as e:
            logger.info("Directory creation failed：%s" % e)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        logger.info("Directory already exists：%s" % str(_dir))


# 随机取任意长度数字字符
def strNum(len=1):
    text = '1234567890'
    text_new = (''.join(random.choice(text) for i in range(len)))
    return text_new


# 随机获取任意长度数字
def long_num(lenth=1):
    text = '1234567890'
    num = (''.join(random.choice(text) for i in range(lenth)))
    return int(num)


# 随机取任意数量字符
def Uppercase(number=1):
    text = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text_new = (''.join(random.choice(text) for i in range(number)))
    return text_new


# 随机取任意数量字符
def lowercase(number=1):
    text = 'abcdefghijklmnopqrstuvwxyz'
    text_new = (''.join(random.choice(text) for i in range(number)))
    return text_new


# 随机取任意数量字符
def chinese(number=1):
    text = '离离原上草一岁一枯荣野火烧不尽春风吹又生远芳侵古道晴翠接荒城又送王孙去萋萋满别情人间四月芳菲尽山寺桃' \
           '花始盛开长恨春归无觅处不知转入此中来天长地久有时尽此恨绵绵无绝期在天愿作比翼鸟在地愿为连理枝' \
           '别有幽愁暗恨生此时无声胜有声同是天涯沦落人相逢何必曾相识细草微风岸危樯独夜舟星垂平野阔月涌大江流名' \
           '岂文章著官应老病休飘飘何所似天地一沙鸥'
    text_new = (''.join(random.choice(text) for i in range(number)))
    return text_new


# 原话记录
def record_line():
    return random.choice(record)


# 半角字符 （缺'_'）
def half_angle(number=1):
    text = r'~`!@#%^&*()-+={[}]|\:;"<.,>?/'
    text_new = (''.join(random.choice(text) for _ in range(number)))
    return text_new


# 全角字符
def full_symbol(number=1):
    text = r'`~！#￥%……&*（）——-+={【}】|、《，》。？、：；"'
    text_new = (''.join(random.choice(text) for _ in range(number)))
    return text_new


# info 多少长度的文本  带空格
def _info(num):
    info = ''
    for i in range(int(num / 5)):
        info = info + '%s ' % (f.pystr(min_chars=4, max_chars=4))
    return info


# get now time
def now_time(format='YYYY/MM/DD HH:mm:ss'):
    curTime = arrow.now()
    t = curTime.format(format)
    return t


# get sys time
def get_system_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


# get anytime format
def getFormatTime(type='days', num=0, format='YYYY/MM/DD HH:mm:ss', tzinfo=None):
    """
    随机获取某一个是的时间
    :param type: days months weeks years
    :param num: 正整数 未来时间，负数 过去时间
    :param format: 时间格式
    :param tzinfo: 时区
    :return:
    """
    if not num:
        num = random.randrange(10000)
    t = arrow.now()
    # t = curTime.to(tz=timezone)
    if type == 'days':
        return t.shift(days=-num).format(format)
    if type == 'weeks':
        return t.shift(weeks=num).format(format)
    if type == 'months':
        return t.shift(months=num).format(format)
    if type == 'years':
        return t.shift(years=num).format(format)


def ipv6():
    return f.ipv6()


def get_time_with_before(format='%Y-%m-%d %H:%M:%S', types="hours", before=1):
    '''
    获取几小时之前,几分钟前
    :param types: hours, minutes
    :param before: 整数值
    :param format:
    :return: 具体时间 %Y-%m-%d %H:%M:%S
    '''
    tn = datetime.datetime.now()
    if types == "minutes":
        t = datetime.timedelta(minutes=before)
    elif types == "hours":
        t = datetime.timedelta(hours=before)
    else:
        return tn.strftime(format)
    strtime = tn - t
    ttime = strtime.strftime(format)
    return ttime


# email
def email():
    email = f.free_email()
    return email


# phone
def phone():
    return f.phone_number()


# 姓名
def name():
    return f.name()


# 性别
def sex():
    return random.choice(["男", "女"])


# 固话
def tel_number():
    numbers = f.phone_number()
    return f"0{numbers[0:3]}-{numbers[3:]}"


# 身份证号
def identity_number():
    return f.ssn(min_age=18, max_age=90)


# 街道信息
def street_address():
    return f.street_address()


def address(level=4):
    """
    :return [省，市，区，详细地址]
    """
    province = random.choice(city_info)
    city = random.choice(province['sub'])
    district = random.choice(city['sub'])
    street = street_address()
    addresses = [province['name'], city['name'], district['name'], street]
    address = []
    for i in range(level):
        address.append(addresses[i])
    return address


# 生成随机经纬度 list
def address_latlng():
    return [int(i) for i in f.latlng()]


# Chrome user-agent info
def chrome_user_agent():
    return f.chrome()


def getValue(dir):
    list = []
    for i in dir.values():
        list.append(i)
    return list


# 返回值为set 和 None
def checkKeys(pre, dir):
    res = set(dir.keys())
    if pre <= res:
        pass
    else:
        dif = pre - res
        return dif


def _string(n1, n2):
    str = f.pystr(min_chars=n1, max_chars=n2)
    return str


def ipv4():
    ip = f.ipv4()
    return ip


def user_agent():
    ua = f.user_agent()
    return ua


# 返回值为set 和 None
def checkValue(dir, key, value):
    if dir[key] != value:
        return key
    else:
        pass


# 生成时间戳
def time_stamp(begin_year=2000, end_year=2022):
    start = (begin_year, 1, 1, 0, 0, 0, 0, 0, 0)
    end = (end_year, 1, 1, 0, 0, 0, 0, 0, 0)
    begin = int(time.mktime(start))
    endless = int(time.mktime(end))
    return random.randint(begin, endless)


# 固定值拆分
def fix_sum(len, sum):
    if isinstance(sum, str):
        sum = int(sum)
    l = []
    for i in range(len):
        if i != len - 1:
            i = random.randrange(0, sum)
            sum = sum - i
            l.append(i)
        else:
            i = sum
            l.append(i)
    return l


# 将列表拆分为n个子列表
def fix_choose(num, l_choose):
    l = []
    for i in range(num):
        if i != num - 1:
            l1 = random.sample(l_choose, k=random.randrange(0, len(l_choose)))
            l.append(l1)
            l_choose = [i for i in l_choose if i not in l1]
    l.append(l_choose)
    return l


# 时分计算
def hm_time():
    hour = random.randrange(0, 24) * 3600
    minu = random.randrange(0, 60) * 60
    tt = hour + minu
    return tt


# 随机获取一段时间内某一时间的时间戳
def strTimeProp(start='1971-01-01', end='2050-12-31', prop=random.random(), frmt='%Y-%m-%d'):
    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))
    ptime = stime + prop * (etime - stime)
    return int(ptime)


def params_list_to_dict(list):
    d = {}
    for i in list:
        d[i] = i
    return d


# 截取24位时间md5
def create_id():
    m = hashlib.md5(str(time.time()).encode('utf-8'))
    return m.hexdigest()[0:25]


# 获取n天后的日期
def dateOperation(strf, day=1):
    today = datetime.datetime.now()
    a = (today + datetime.timedelta(day)).strftime(strf)
    return str(a)


# 截取字符串
def cut(str, i):
    '''
    :param str: 传入的字符串
    :param i:截取的位数
    :return:截取后的字符串
    '''
    return str[:i]


def past_date():
    return datetime.datetime.strftime(f.date_time(), '%Y/%m/%d')


# 随机生成industry_id
def random_industrys():
    with open(os.path.realpath(os.path.abspath('./.env'))) as env:
        for line in env.read().splitlines():
            if 'industrys' in line:
                return random.choice(line.split(" ")[2].split(',')[0: -1])


if __name__ == '__main__':
    pass
