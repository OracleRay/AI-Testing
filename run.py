# -*- coding: utf-8 -*-
import time
import sys
import env_init
import os.path
from utils import send_email

os.environ["HRUN_LOG_LEVEL"] = "WARNING"  # 只显示 WARNING 及以上日志信息

if __name__ == '__main__':
    import logging
    try:
        # 调用登录接口,获取token并重写.env文件
        if len(sys.argv) > 1:
            test_env = sys.argv[1]
            # production environment
            if sys.argv[1] == 'saas':
                test_env = 'saas'
            # pre-production environment
            elif sys.argv[1] == 'pre':
                test_env = 'pre'
            # test environment
            elif sys.argv[1] == 'test':
                test_env = 'test'
        else:
            test_env = 'test'
        env_init.env_init(test_env)
        # 获取当前时间，转换成固定格式
        nowTime = time.localtime(int(time.time()))
        otherStyleTime = time.strftime("%Y-%m-%d-%H-%M-%S", nowTime)
        os.system("pytest "
                  "ai_tests/"
                  "  -m " + test_env + " --alluredir=allure_report --reruns 1")
    except Exception as e:
        logging.exception(f"接口脚本出错,请检查{e}")
        # send_email.mail("接口脚本出错,请检查", "")
        raise Exception
