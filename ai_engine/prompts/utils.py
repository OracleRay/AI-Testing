import json
import os


def find_related_test_data(api_name: str, api_url: str) -> str:
    """
    查找与当前API测试相关的JSON数据文件

    Args:
        api_name: API名称
        api_url: API URL

    Returns:
        str: 相关测试数据的JSON字符串，如果没有找到则返回空字符串
    """
    try:
        # 定义API与测试数据的映射关系
        api_data_mapping = {
            # 用户管理相关API
            "create_user": "users.json",
            "update_user": "users.json",
            "query_user": "users.json",
            "新增账号": "users.json",
            "更新账号": "users.json",
            "查询账号": "users.json",

            # 项目管理相关API
            "create_project": "projects.json",
            "update_project": "projects.json",
            "query_project": "projects.json",
            "新增项目": "projects.json",
            "更新项目": "projects.json",
            "查询项目": "projects.json",

            # 问卷管理相关API
            "create_survey": "surveys.json",
            "update_survey": "surveys.json",
            "query_survey": "surveys.json",
            "新增问卷": "surveys.json",
            "更新问卷": "surveys.json",
            "查询问卷": "surveys.json",

            # 工单管理相关API
            "create_ticket": "tickets.json",
            "update_ticket": "tickets.json",
            "query_ticket": "tickets.json",
            "新增工单": "tickets.json",
            "更新工单": "tickets.json",
            "查询工单": "tickets.json"
        }

        # 查找对应的测试数据文件名
        test_data_file = None

        # 首先尝试精确匹配API名称
        if api_name in api_data_mapping:
            test_data_file = api_data_mapping[api_name]
        else:
            # 尝试模糊匹配
            for key, value in api_data_mapping.items():
                if key.lower() in api_name.lower() or api_name.lower() in key.lower():
                    test_data_file = value
                    break

                # 如果还是没找到，尝试从URL推断
                if not test_data_file:
                    if "user" in api_url.lower():
                        test_data_file = "users.json"
                    elif "project" in api_url.lower():
                        test_data_file = "projects.json"
                    elif "survey" in api_url.lower() or "qdes" in api_url.lower():
                        test_data_file = "surveys.json"
                    elif "ticket" in api_url.lower():
                        test_data_file = "tickets.json"

        # 如果找到了测试数据文件，尝试加载
        if test_data_file:
            # 尝试多个可能的路径
            possible_paths = [
                f"prompts/test_data/{test_data_file}",
                f"ai_engine/prompts/test_data/{test_data_file}",
                f"../ai_engine/prompts/test_data/{test_data_file}",
                f"../../ai_engine/prompts/test_data/{test_data_file}"
            ]

            test_data = None
            for test_data_path in possible_paths:
                if os.path.exists(test_data_path):
                    try:
                        with open(test_data_path, 'r', encoding='utf-8') as f:
                            test_data = json.load(f)
                        print(f"成功加载测试数据文件: {test_data_path}")
                        break
                    except Exception as e:
                        print(f"读取文件 {test_data_path} 时出错: {e}")
                        continue

            # 格式化测试数据用于prompt
            if test_data:
                formatted_data = json.dumps(test_data, ensure_ascii=False, indent=2)
                return f"""
                相关测试数据：
                {formatted_data}

                使用说明：
                - 请基于上述测试数据生成相关的测试用例
                - 确保测试数据的一致性和连贯性
                - 考虑数据依赖关系
                """

        return ""

    except Exception as e:
        print(f"查找测试数据时出错: {e}")
        return ""


def analyze_api_operation_type(api_name: str, api_url: str) -> str:
    """
    分析API操作类型
    
    Args:
        api_name: API名称
        api_url: API URL
        
    Returns:
        str: 操作类型 (CREATE, READ, UPDATE, DELETE, OTHER)
    """
    # 根据API名称和URL分析操作类型
    name_lower = api_name.lower()
    url_lower = api_url.lower()
    
    # 创建操作关键词
    create_keywords = ['创建', '新增', '添加', 'create', 'add', 'insert', 'post']
    # 查询操作关键词  
    read_keywords = ['查询', '获取', '列表', '详情', 'get', 'query', 'list', 'detail', 'find']
    # 更新操作关键词
    update_keywords = ['更新', '修改', '编辑', 'update', 'modify', 'edit', 'put', 'patch']
    # 删除操作关键词
    delete_keywords = ['删除', '移除', 'delete', 'remove', 'del']
    
    # 检查名称中的关键词
    for keyword in create_keywords:
        if keyword in name_lower:
            return "CREATE"
    for keyword in read_keywords:
        if keyword in name_lower:
            return "READ"
    for keyword in update_keywords:
        if keyword in name_lower:
            return "UPDATE"
    for keyword in delete_keywords:
        if keyword in name_lower:
            return "DELETE"
    
    # 检查URL中的关键词
    for keyword in create_keywords:
        if keyword in url_lower:
            return "CREATE"
    for keyword in read_keywords:
        if keyword in url_lower:
            return "READ"
    for keyword in update_keywords:
        if keyword in url_lower:
            return "UPDATE"
    for keyword in delete_keywords:
        if keyword in url_lower:
            return "DELETE"
    
    # 默认返回OTHER
    return "OTHER"


def has_error_response_in_spec(api_spec: str) -> bool:
    """检测API规范中是否包含错误响应信息"""
    api_spec_lower = api_spec.lower()

    # 检查是否包含错误响应相关的关键词
    error_indicators = [
        '错误响应', 'error response', 'error code', '错误码', 'status code',
        '失败', 'fail', 'error', '异常', 'exception',
        '400', '401', '403', '404', '500', '502', '503',
        '错误示例', 'error example', '失败示例', 'failure example',
        '失败响应', 'failure response'
    ]

    # 检查是否包含失败响应示例（只要包含"fail"字段就认为是错误响应）
    has_fail_example = 'fail' in api_spec_lower
    
    # 检查是否包含错误码数字
    import re
    error_codes = re.findall(r'\b(?:4\d{2}|5\d{2}|[1-9]\d{2})\b', api_spec)
    has_error_codes = len(error_codes) > 0

    return any(indicator in api_spec_lower for indicator in error_indicators) or has_fail_example or has_error_codes