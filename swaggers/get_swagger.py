import requests
import re
import json
import logging
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def extract_swagger_schema(api_url):
    """
    从API文档页面提取swagger schema信息
    
    Args:
        api_url (str): API文档的URL
    
    Returns:
        dict: 提取的schema信息
    """
    try:
        # 发送GET请求获取HTML文档
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()  # 检查请求是否成功
        html_content = response.text
        
        # 使用BeautifulSoup解析HTML中的script标签
        schemas_bs = extract_schemas_with_beautifulsoup(html_content)

        swagger_paths = []
        for idx, schema in enumerate(schemas_bs, start=1):
            file_path = f"swaggers/swagger_{idx}.json"
            save_schemas_to_file(schema, filename=file_path)
            swagger_paths.append(file_path)

        return swagger_paths
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except Exception as e:
        print(f"解析失败: {e}")
        return None


def extract_schemas_with_beautifulsoup(html_content):
    """
    使用BeautifulSoup解析HTML中的script标签
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    schemas = []
    
    # 查找所有script标签
    script_tags = soup.find_all('script')
    
    for script in script_tags:
        if script.string:
            # 在script内容中查找schema定义
            pattern = r'const\s+(schema_\w+)\s*=\s*(\{.*?\});'
            matches = re.findall(pattern, script.string, re.DOTALL)

            for schema_info in matches:
                for info in schema_info:
                    if "openapi" in info:
                        try:
                            schema_dict = json.loads(info)
                            schemas.append(schema_dict)
                        except json.JSONDecodeError:
                            logger.info("json格式转化失败")

    return schemas

def save_schemas_to_file(schemas, filename):
    """
    将提取的schemas保存到文件
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(schemas, f, indent=2, ensure_ascii=False)
        logger.info(f"已保存 {filename}")
    except Exception as e:
        raise f"保存文件失败: {e}"
