import requests
import urllib3
from loguru import logger
from configs.config import ConfigManager

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 倍市得系统登录
def bestcem_login(test_env):
    base_url, plat_config = ConfigManager.get_openplatform('open_new', test_env)
    url = f"{base_url['bestcem']}/api/authorize/v2/token/"
    payload = {
        'is_home_page': False,
        'org_code': plat_config["baseorg_code"],
        'password': plat_config["basepassword"],
        'user_name': plat_config["baseuser"],
    }
    res = requests.post(url=url, json=payload, verify=False)
    if res.json()['code'] == 0:
        token = f"{res.json()['data']['token']}"
        return token
    else:
        logger.error(f"bestcem_login url:{url}")
        logger.error(f"bestcem_login payload:{payload}")
        logger.error(f"bestcem_login resp:{res.json()}")
        exit(1)

# 开放平台登录账号
def openplatform_login(test_env):
    # 获取配置
    base_url, plat_config = ConfigManager.get_openplatform('open_new', test_env)

    url = f"{base_url['openplatform']}/api/open/v1/auth/platform/"
    payload = {
        'org_id': plat_config["org_id"],
        'secret_key': plat_config["secret_key"],
    }
    res = requests.post(url=url, json=payload, verify=False)
    logger.info(f"openplatform_login {res.json()}")
    access_token = f"Bearer {res.json()['data']['access_token']}"
    if res.json()['code'] == 0:
        return access_token
    else:
        logger.error(f"openplatform_login resp:{res.json()}")
        exit(1)


def env_init(test_env):
    """
    加载环境信息
    :param test_env: 当前测试环境：test、saas、pre
    :return: 返回动态信息字典
    """
    token = bestcem_login(test_env)
    access_token = openplatform_login(test_env)
    dynamic_info = {
        'env': test_env,
        'token': token,
        'access_token': access_token
    }
    if test_env == 'test':
        # 写入.env文件，仅写动态信息
        with open('.env', 'w', encoding='utf-8') as f:
            for k, v in dynamic_info.items():
                f.write(f"{k}={v}\n")
        logger.info(f"[env_init] 已写入 .env 文件（仅动态信息），当前测试环境为：{test_env}")
    else:
        # saas/pre环境，动态信息存入ConfigManager
        ConfigManager.set_dynamic_info(test_env, dynamic_info)
        logger.info(f"[env_init 动态信息已加载入内存，当前测试环境为：{test_env}")
    return dynamic_info

if __name__ == '__main__':
    env_init("test")

