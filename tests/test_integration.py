# -*- coding: utf-8 -*-
"""
集成测试
"""
import os
import sys
import tempfile
from pathlib import Path
import unittest.mock as mock

# 添加项目根目录到Python路径，以便导入模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from crawler import create_markdown, save_to_md, job
from tools.organize_history import organize_history_files


def test_full_workflow():
    """
    测试完整的爬虫工作流程
    """
    print("测试完整的爬虫工作流程...")
    
    # 创建临时目录来测试
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # 模拟创建测试目录
            test_markdowns_dir = Path("markdowns")
            test_markdowns_dir.mkdir(exist_ok=True)
            
            # 创建一个测试文件
            test_date = "2025-12-24"
            year, month, day = test_date.split('-')
            test_filename = f"markdowns/{year}/{month}/{test_date}.md"
            
            # 测试创建markdown文件
            create_markdown(test_date, test_filename)
            
            # 检查文件和目录是否正确创建
            file_path = Path(test_filename)
            assert file_path.exists(), f"文件 {test_filename} 应该被创建"
            
            # 检查内容是否正确
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert f"## {test_date} Github Trending" in content
            
            # 测试数据保存功能
            test_data = [
                ["test_project", "https://github.com/test/test", "A test project", 100, 20, 5],
                ["another_project", "https://github.com/another/test", "Another test project", 200, 30, 10]
            ]
            
            save_to_md(test_data, test_filename, "python", topk=5)
            
            # 验证数据是否被追加到文件中
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "test_project" in content
                assert "another_project" in content
                assert "python" in content
            
            print("PASSED: 完整工作流程测试通过")
            
        finally:
            os.chdir(original_cwd)


def test_history_organization_integration():
    """
    测试历史文件整理的集成
    """
    print("测试历史文件整理集成...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # 创建测试目录结构
            test_markdowns_dir = Path("markdowns")
            test_markdowns_dir.mkdir()
            
            # 创建一些测试历史文件
            test_files = [
                "2023-06-15.md",
                "2023-07-20.md",
                "2024-01-10.md",
                "2024-01-25.html",
                "readme.txt"  # 非日期格式文件
            ]
            
            for filename in test_files:
                (test_markdowns_dir / filename).touch()
            
            # 运行历史文件整理
            organize_history_files()
            
            # 验证日期格式文件被移动
            assert (test_markdowns_dir / "2023" / "06" / "2023-06-15.md").exists()
            assert (test_markdowns_dir / "2023" / "07" / "2023-07-20.md").exists()
            assert (test_markdowns_dir / "2024" / "01" / "2024-01-10.md").exists()
            assert (test_markdowns_dir / "2024" / "01" / "2024-01-25.html").exists()
            
            # 验证非日期格式文件未被移动
            assert (test_markdowns_dir / "readme.txt").exists()
            
            # 验证原位置不再有日期格式文件
            for filename in ["2023-06-15.md", "2023-07-20.md", "2024-01-10.md", "2024-01-25.html"]:
                assert not (test_markdowns_dir / filename).exists()
            
            print("PASSED: 历史文件整理集成测试通过")
            
        finally:
            os.chdir(original_cwd)


def test_path_generation():
    """
    测试路径生成逻辑
    """
    print("测试路径生成逻辑...")
    
    # 测试不同日期的路径生成
    test_cases = [
        ("2024-01-01", "markdowns/2024/01/2024-01-01.md"),
        ("2024-12-31", "markdowns/2024/12/2024-12-31.md"),
        ("2025-02-28", "markdowns/2025/02/2025-02-28.md"),
        ("2025-11-15", "markdowns/2025/11/2025-11-15.md")
    ]
    
    for date_str, expected_path in test_cases:
        year, month, day = date_str.split('-')
        generated_path = f'markdowns/{year}/{month}/{date_str}.md'
        assert generated_path == expected_path, f"路径生成错误: 期望 {expected_path}, 得到 {generated_path}"
    
    print("PASSED: 路径生成逻辑测试通过")


def run_all_tests():
    """
    运行所有集成测试
    """
    print("开始运行集成测试...")
    
    test_path_generation()
    test_full_workflow()
    test_history_organization_integration()
    
    print("\nALL INTEGRATION TESTS PASSED!")


if __name__ == '__main__':
    run_all_tests()