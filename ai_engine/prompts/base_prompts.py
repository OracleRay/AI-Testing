from utils.load_file import read_file

class UserQueryPrompt:
    """AI提示词模板类"""

    @staticmethod
    def get_test_cases_prompt(api_spec: str) -> str:
        """获取生成测试用例的提示词"""

        error_code = read_file("swaggers/error_code.md")

        return f"""
        你是一个专业的API测试工程师，请基于以下JSON格式的API规范文档和markdown格式的错误码生成全面的测试数据。

        **重要提醒1：生成的数据必须是纯JSON格式，严禁使用任何编程语法！**
        **重要提醒2：生成失败用例时，要根据不同类型的错误在错误码中找到对应的错误码，不可随机生成！**

        API规范文档（JSON格式）：
        ```
        {api_spec}
        ```
        
        错误码（markdown格式）：
        ```
        {error_code}
        ```

        请生成以下类型的测试用例：
        - 成功用例：正常操作、边界值操作
        - 失败用例：参数缺失、参数格式错误、参数值非法/越界、业务逻辑错误

        请严格按照以下JSON格式返回测试用例数据：
        {{
            "success": [
                ["正常操作", {{ "param1: value1" }}, 0],
                ["边界值操作", {{ "param1: value2" }}, 0]
            ],
            "error": [
                ["参数错误", {{ "param1: invalid" }}, 错误码],
                ["格式错误", {{ "param1: wrong_format" }}, 错误码]
            ]
        }}
        
        举例：
        "success": [
            ["正常操作", {{"id": "123", "phone": "", "msg": "Hello"}}, 0]
        ]
        "error": [
            ["id缺失", {{"id": "", "phone": "138122345678", "msg": "adfasdfz"}}, 206]
        ]

        要求：
        1. 仔细分析API文档，提取准确的参数和响应信息
        2. 参考例子，生成严格符合模板格式的JSON数据，测试用例的类型为：[[字符串类型,字典类型,整型],[字符串类型,字典类型,整型]]
        3. 成功用例至少生成5条, 失败用例至少生成10条，并且尽可能生成测试覆盖率高的测试用例
        4. API文档中query_required字段代表哪些query参数是必填项，要根据必填参数和非必填参数调整成功用例和失败用例的参数具体值
        5. 生成测试用例时，不能打乱参数的原本顺序
        6. 生成空参数时，不要生成None或者null，用""代替
        7. 切记不要忘了状态码（错误码）
        """


    @staticmethod
    def get_system_prompt() -> str:
        """获取系统提示词"""
        return "你是一个专业的API测试工程师，请严格按照要求生成JSON格式的测试数据。"


class PromptConfig:
    """提示词配置类，用于管理不同类型的提示词"""

    # 可以在这里添加更多的配置选项
    DEFAULT_SYSTEM_PROMPT = "你是一个专业的API测试工程师，请严格按照要求生成JSON格式的测试数据。"

    # 不同场景的系统提示词
    SYSTEM_PROMPTS = {
        "test_generation": "你是一个专业的API测试工程师，请基于API规范生成完整的测试用例。",
        "assertion_generation": "你是一个专业的API测试工程师，请基于API响应格式生成HttpRunner风格的断言。",
        "data_generation": "你是一个专业的API测试工程师，请生成符合API规范的测试数据。"
    }

    @classmethod
    def get_system_prompt(cls, prompt_type: str = "test_generation") -> str:
        """获取指定类型的系统提示词"""
        return cls.SYSTEM_PROMPTS.get(prompt_type, cls.DEFAULT_SYSTEM_PROMPT)