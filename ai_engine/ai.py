import json
import logging
import openai
from typing import List, Dict, Any, Optional
from configs.config import ConfigManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeepSeekAI(object):
    def __init__(self):
        """
        初始化DeepSeek测试生成器

        Args:
            deepseek_api_key: DeepSeek API密钥
            model_name: 模型名称，如果为None则从配置文件读取
        """
        # 配置OpenAI 0.28.x API
        ai_config = ConfigManager.get().get('ai_config', {})
        model_name = ai_config.get('model_name', 'deepseek-coder')
        openai.api_key = ai_config.get('api_key', '')
        openai.api_base = "https://api.deepseek.com"
        
        self.model_name = model_name
        self.generation_config = {
            "temperature": ai_config.get('temperature', 0.7),
            "top_p": ai_config.get('top_p', 0.8),
            "max_tokens": ai_config.get('max_tokens', 8192),
        }

    def _fix_javascript_syntax(self, response_text: str) -> str:
        """修复响应文本中的JavaScript语法问题"""
        import re
        
        # 修复 .repeat() 语法
        # 将 "a".repeat(100) 替换为重复的字符串
        def replace_repeat(match):
            char = match.group(1)
            count = int(match.group(2))
            # 限制重复次数避免过长字符串
            count = min(count, 200)
            return f'"{char * count}"'
        
        response_text = re.sub(r'"([^"]+)"\.repeat\((\d+)\)', replace_repeat, response_text)
        
        # 修复其他常见的JavaScript语法
        # 移除 .length 属性
        response_text = re.sub(r'\.length', '', response_text)
        
        # 修复字符串拼接 
        response_text = re.sub(r'"([^"]+)"\s*\+\s*"([^"]+)"', r'"\1\2"', response_text)
        
        return response_text

    def _ai_response(self, prompt: str, generation_config: Dict[str, Any], prompt_type: str = "test_generation") -> \
    List[Dict[str, Any]]:
        """调用DeepSeek AI获取响应"""
        try:
            from .prompts.base_prompts import PromptConfig
            
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": PromptConfig.get_system_prompt(prompt_type)},
                    {"role": "user", "content": prompt}
                ],
                **generation_config
            )

            # 获取响应文本
            response_text = response.choices[0].message.content.strip()  # type: ignore

            # 清理响应文本，移除markdown代码块标记
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            # 预处理：修复常见的JavaScript语法问题
            response_text = self._fix_javascript_syntax(response_text)

            # 解析JSON
            return json.loads(response_text)
        except Exception as e:
            logger.error(f"AI响应解析失败: {e}")
            logger.error(f"原始响应: {response_text if 'response_text' in locals() else 'N/A'}")
            raise