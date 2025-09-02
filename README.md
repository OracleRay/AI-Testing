# AI自动化接口测试

## 概述

这是一个基于AI技术的自动化接口测试项目，通过DeepSeek-Coder大模型分析Swagger API文档，自动生成完整的HttpRunner风格的接口测试用例。项目支持多环境配置（test/pre/saas），具备AES加解密、签名验证等企业级功能，可以实现从Swagger文档解析到测试代码生成的全自动化流程。

## 项目结构

- **ai_engine/**: AI引擎核心代码
  - **ai.py**: DeepSeek AI模型封装，负责调用AI生成测试用例
  - **generator.py**: 测试数据生成器，基于API规范生成测试用例
  - **prompts/**: AI提示词模板和配置
    - **base_prompts.py**: 核心提示词模板，定义AI生成测试用例的规则
    - **test_data/**: 测试所需的固定数据（如用户信息等）
    - **utils.py**: 提示词相关工具函数
- **configs/**: 配置管理
  - **config.py**: 配置管理器，支持多环境配置和动态信息管理
  - **config.yaml**: 主配置文件，包含AI配置、环境配置、认证信息等
- **swaggers/**: Swagger文档处理
  - **get_swagger.py**: 从API文档页面提取Swagger schema
  - **gen_apidoc.py**: 解析Swagger文档生成API数据
  - **swagger2/**: Swagger文档解析库
- **testcases/**: 生成的测试代码存储目录
- **template/**: 测试代码模板文件
  - **template_common.txt**: HttpRunner测试代码通用模板
- **utils/**: 工具类库
  - **aes_utils.py**: AES加解密工具
  - **com_utils.py**: 通用工具函数
  - **log.py**: 日志配置
  - **city_info/**: 城市信息数据

## 快速开始


### 配置设置
1. **AI配置**：编辑 `configs/config.yaml`，配置DeepSeek API Key：
   ```yaml
   ai_config:
     model_name: "deepseek-coder"
     api_key: "your-deepseek-api-key"
     temperature: 0.7
     max_tokens: 8192
   ```

2. **环境配置**：根据实际环境修改 `configs/config.yaml` 中的各环境配置信息。
3. **代码模板**：根据实际情况修改 `template/template_common.txt` 文件

### 生成测试代码
1. **自动获取Swagger文档并生成测试代码**：
   ```bash
   # 从指定URL获取Swagger文档并生成所有API的测试代码
   python main.py --url "http://your-api-doc-url/api/doc/"
   
   # 为指定API路径生成测试代码
   python main.py --api "/api/specific/path" --url "http://your-api-doc-url/api/doc/"
   ```

2. **使用本地Swagger文档并生成所有api接口的测试代码**：
   ```bash
   # 如果本地已有swagger_*.json文件，直接生成测试代码
   python main.py
   ```

### 运行测试
```bash
# 运行测试（默认test环境）
python run.py

# 指定环境运行测试
python run.py test    # 测试环境
python run.py pre     # 预发布环境
python run.py saas    # 生产环境
```

### 查看测试报告
```bash
# 生成并查看Allure测试报告
allure serve allure_report
```


## 工作流程

### 1. Swagger文档获取
```
API文档URL → get_swagger.py → 提取schema → 保存为swagger_*.json
```

### 2. API数据解析
```
swagger_*.json → gen_apidoc.py → 解析API结构 → 生成api.json
```

### 3. AI测试生成
```
api.json → AI模型分析 → 生成测试用例数据 → 填充模板 → 生成.py测试文件
```

### 4. 测试执行
```
环境初始化 → 获取认证token → 执行测试用例 → 生成测试报告
```
