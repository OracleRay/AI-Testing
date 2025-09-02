import yaml
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
import os

class ConfigManager:
    _config = None
    _env_loaded = False
    _test_env = 'test'
    _dynamic_info = None  #存储动态配置信息

    @classmethod
    def load_env(cls):
        """加载.env文件中的环境变量"""
        if cls._env_loaded:
            return
        
        # 查找.env文件
        base_path = Path(__file__).resolve().parent.parent
        env_path = base_path / ".env"
        
        if env_path.exists():
            load_dotenv(env_path, verbose=True)
            cls._env_loaded = True
        else:
            logger.info(f".env文件不存在: {env_path}")

    @classmethod
    def load(cls, path=None):
        """从指定路径或默认路径加载配置文件。"""
        if cls._config is not None:
            return

        # 加载.env文件
        cls.load_env()

        # 只在test环境下加载.env
        if cls._test_env == 'test':
            cls.load_env()

        # 默认读取与 config.py 同级目录下的 config.yaml
        base_path = Path(__file__).resolve().parent
        config_path = Path(path) if path else base_path / "config.yaml"

        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as file:
            cls._config = yaml.safe_load(file)

    @classmethod
    def get(cls):
        """获取配置，如果未加载则延迟加载。"""
        if cls._config is None:
            cls.load()
        return cls._config

    @classmethod
    def reload(cls):
        """重新加载配置文件。"""
        cls._config = None
        cls._env_loaded = False
        return cls.load()

    @classmethod
    def get_openplatform(cls, open_type='open_new', test_env=None):
        """获取指定 open_type 的 base_url 和 openplatform 配置。"""
        config_data = cls.get()
        if not config_data or open_type not in config_data:
            raise KeyError(f"配置中不存在 {open_type}")
        
        if 'base_url' not in config_data[open_type] or 'openplatform' not in config_data[open_type]:
            raise KeyError(f"配置中不存在 {open_type} 的 base_url 或 openplatform")
        
        if not test_env:
            test_env = cls._test_env
        
        base_url = config_data[open_type]['base_url'][test_env]
        openplatform = config_data[open_type]['openplatform'][test_env]
        
        return base_url, openplatform

    @classmethod
    def set_dynamic_info(cls, test_env, info_dict):
        """设置动态信息（如access_token等）"""
        cls._test_env = test_env
        cls._dynamic_info = info_dict

    @classmethod
    def get_dynamic_info(cls, key, default=None):
        """获取动态信息（如access_token等），优先内存（saas/pre），test环境优先os.environ"""
        env = cls._test_env
        if env == 'test':
            return os.getenv(key, default)
        else:
            if cls._dynamic_info and key in cls._dynamic_info:
                return cls._dynamic_info[key]
            raise KeyError(f"配置中不存在 {key}, 请检查！")

    @classmethod
    def get_ai_config(cls):
        """获取AI模型配置"""
        config_data = cls.get()
        if not config_data or 'ai_config' not in config_data:
            raise KeyError("配置中不存在 ai_config")
        
        ai_config = config_data['ai_config']
        
        # 优先从环境变量获取API key，如果没有则使用配置文件中的
        api_key = os.getenv('DEEPSEEK_API_KEY', ai_config.get('api_key', ''))
        
        return {
            'model_name': ai_config.get('model_name', 'deepseek-coder'),
            'temperature': ai_config.get('temperature', 0.7),
            'top_p': ai_config.get('top_p', 0.8),
            'max_tokens': ai_config.get('max_tokens', 8192),
            'api_key': api_key
        }