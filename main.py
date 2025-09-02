import glob
import logging
import argparse

from convert_py import generate_tests_for_apis
from swaggers.gen_apidoc import get_apidoc
from swaggers.get_swagger import extract_swagger_schema

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='生成API测试用例和断言')
    parser.add_argument('--api', type=str, default='', help='指定API路径以单独生成测试用例和断言')
    parser.add_argument('--url', type=str, default="http://localhost:5000/api/doc/", help='存放swagger的url')
    args = parser.parse_args()

    paths = []  # 存放swagger文档的列表
    pattern = "swaggers/swagger_[0-9]*.json"
    if not glob.glob(pattern):
        # 提取swagger文档
        logger.info(f"正在由 {args.url} 生成swagger文档...")
        paths = extract_swagger_schema(args.url)
        logger.info(f"{args.url} 共检测到 {len(paths)} 个swagger文档，已生成完毕")
    else:
        paths = glob.glob(pattern)
        logger.info(f"本地存在swagger文档，将使用本地文档...")

    # for path in paths:  # 遍历每一个swagger文档

    # 由第一个swagger文档api文档
    api_list = get_apidoc(paths[0])

    # 生成测试代码
    if api_list:
        # 若未指定args.api，则根据swagger接口文档全部生成测试代码
        test_results = generate_tests_for_apis(api_list, args.api)
    else:
        logger.warning("没有从api.json文件中读取到API数据")