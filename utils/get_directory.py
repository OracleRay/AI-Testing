#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# 获取common目录
UTILS_DIR = os.path.dirname(__file__)
# 截取项目路径
PROJECT_DIR = os.path.dirname(UTILS_DIR)
# 获取data source目录
API_DIR = f'{PROJECT_DIR}/api'
# 获取data result目录
DATA_RESULT_DIR = f'{PROJECT_DIR}/data/result'

print(API_DIR)
