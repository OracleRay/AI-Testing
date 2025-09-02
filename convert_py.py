import json
import logging
import os
import datetime

from ai_engine.generator import GenerateTestDatas
from utils.load_file import read_json, read_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_python_file(api_data):
    """根据API数据生成Python测试文件"""
    api_name = api_data['name'].replace('/', '_')
    try:
        # 根据HTTP方法选择模板
        method = api_data['method'].lower()
        template_path = "template/template_common.txt"

        # 读取模板内容
        template_content = read_file(template_path)
        if not template_content:
            logger.error(f"无法读取模板文件: {template_path}")
            return False

        # 格式化测试用例
        success_cases = str(api_data.get('success_cases', [])).replace("),", "),\n")
        error_cases = str(api_data.get('error_cases', [])).replace("),", "),\n")

        filled_content = template_content
        if method == 'get':
            filled_content = filled_content.replace('${with}', 'with_data')
        else:
            filled_content = filled_content.replace('${with}', 'with_json')


        # 使用简单的字符串替换，避免Template解析问题
        filled_content = filled_content.replace('${feature}', api_name)
        filled_content = filled_content.replace('${base_url}', api_data['host'])
        filled_content = filled_content.replace('${path}', api_data['path'])
        filled_content = filled_content.replace('${method}', method)
        filled_content = filled_content.replace('${generate_time}', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        filled_content = filled_content.replace('${success_cases}', success_cases)
        filled_content = filled_content.replace('${error_cases}', error_cases)
        # 保持这些变量不变，它们会在运行时被处理
        # ${request_data}, ${response}, ${assert_code}, ${hooks_open_request($request,True,False)} 等
        
        # 创建输出目录
        output_dir = "testcases"
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成文件名
        output_filename = f"test_{api_name}_{method}.py"
        output_path = os.path.join(output_dir, output_filename)
        
        # 保存文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(filled_content)
        
        logger.info(f"成功生成Python测试文件: {output_path} \n")
        return True
        
    except Exception as e:
        logger.error(f"生成{api_name}api测试脚本时出错: {e}")
        return False


def generate_tests_for_apis(api_list, specific_api_path=None):
    """为API列表中的每个API生成测试用例和断言，如果指定了API路径，则只生成该API的测试用例和断言"""
    results = []
    target_apis = []
    
    if specific_api_path:
        for api in api_list:
            if api.get('path') == specific_api_path:
                target_apis.append(api)
                break
        if not target_apis:
            logger.warning(f"未找到路径为 {specific_api_path} 的API")
            return results
    else:
        target_apis = api_list
    
    for api in target_apis:
        api_name = api.get('name', '未知API')
        logger.info(f"正在为API {api_name} 生成测试代码...")
        
        api_spec = json.dumps(api, ensure_ascii=False, indent=2)
        generator = GenerateTestDatas(api_spec)
        test_cases = generator.generate_test_cases()
        
        # 格式化测试用例和断言
        success_cases = [tuple(case) for case in test_cases.get('success', [])]
        error_cases = [tuple(case) for case in test_cases.get('error', [])]

        res = {
            'name': api_name,
            'method': api.get('method', 'get'),
            'host': api.get('host', 'http://autoopen.xm-mysql.bestcem.com'),
            'path': api.get('path', '/unknown/path'),
            'query': api.get('query', ''),
            'json': api.get('json', ''),
            'success_cases': success_cases,
            'error_cases': error_cases
        }
        results.append(res)

        # 生成python文件
        generate_python_file(res)

    return results
