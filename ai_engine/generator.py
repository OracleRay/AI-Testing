import logging

from ai_engine.prompts.base_prompts import UserQueryPrompt
from ai_engine.ai import DeepSeekAI
from typing import List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GenerateTestDatas(DeepSeekAI):
    def __init__(self, api_spec: str):
        super().__init__()
        self.api_spec = api_spec
        self.prompt = UserQueryPrompt.get_test_cases_prompt(api_spec)

    def generate_test_cases(self) -> List[dict]:
        try:
            test_cases_data = self._ai_response(self.prompt, self.generation_config, "test_generation")

            return test_cases_data

        except Exception as e:
            raise OSError(f"DeepSeek生成测试用例失败: {e}")

if __name__ == "__main__":
    # 断言生成器的测试代码
    api_spec = """{
        "id": "3400c243559b424e9c595ddaf94f7dba",
        "name": "获取投放链接",
        "method": "post",
        "path": "/api/open/v1/deliver/third/",
        "url": "http://https://autoopen.xm-mysql.bestcem.com/api/open/v1/deliver/third/",
        "headers": {
          "Content-Type": "application/json"
        },
        "paths": {},
        "query": {},
        "json": {
          "type": "object",
          "properties": {
            "survey_id": {
              "type": "string",
              "description": "问卷ID，可以是单个ID或ID列表",
              "example": "507f1f77bcf86cd799439011"
            },
            "status": {
              "type": "integer",
              "description": "状态，可选参数",
              "example": 1
            },
            "page": {
              "type": "integer",
              "description": "页码，默认值为1",
              "example": 1
            },
            "rowsPerPage": {
              "type": "integer",
              "description": "每页行数，默认值为10",
              "example": 10
            },
            "ttype": {
              "type": "integer",
              "description": "类型，可选参数，区分总部或门店",
              "example": 1
            }
          },
          "required": [
            "survey_id"
          ]
        },
        "form": {},
        "formData": {},
        "response": {
          "200": {
            "type": "object",
            "properties": {
              "code": {
                "type": "integer",
                "description": "状态码",
                "example": 0
              },
              "data": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer",
                    "description": "总条数",
                    "example": 18
                  },
                  "rows": {
                    "type": "array",
                    "description": "投放链接总数",
                    "example": [
                      {
                        "link_total": 100,
                        "link_rows": [
                          {
                            "level_code": "",
                            "title": "",
                            "link": "https://bestcem.com/t/5RXAPI",
                            "survey_id": "6074030daace7000091bea32",
                            "deliver_id": "60740312f9f4f6001bcf6aec",
                            "type": 0
                          }
                        ]
                      }
                    ]
                  }
                }
              }
            }
          }
        }
        }"""
    generator = GenerateTestDatas(api_spec)
    test_cases, assertions = generator.generate_test_cases()
    logger.info("生成成功")
