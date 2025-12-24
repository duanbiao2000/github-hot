# 测试套件

本项目包含以下测试模块：

## 测试文件说明

- `test_crawler.py` - 测试爬虫核心功能，包括文件创建、目录结构生成等
- `test_organize_history.py` - 测试历史文件整理功能
- `test_integration.py` - 集成测试，验证整个工作流程
- `run_all_tests.py` - 运行所有测试的入口脚本

## 运行测试

要运行所有测试，可以执行：

```bash
python tests/run_all_tests.py
```

或者单独运行某个测试：

```bash
python tests/test_crawler.py
```

## 测试覆盖范围

- 功能测试：验证爬虫功能是否按预期工作
- 集成测试：验证整个系统组件间的协作
- 路径生成测试：验证年/月目录结构的正确性
- 文件操作测试：验证文件创建和移动功能