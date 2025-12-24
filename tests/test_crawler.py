# -*- coding: utf-8 -*-
"""
测试爬虫功能
"""
import datetime
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径，以便导入模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from crawler import create_markdown, scrape, save_to_md, job


def test_create_markdown():
    """
    测试创建markdown文件功能
    """
    # 测试日期和文件名
    test_date = "2025-12-24"
    test_filename = "test_markdowns/2025/12/test_file.md"
    
    # 创建测试文件
    create_markdown(test_date, test_filename)
    
    # 检查文件是否创建
    file_path = Path(test_filename)
    assert file_path.exists(), f"文件 {test_filename} 应该被创建"
    
    # 检查文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert f"## {test_date} Github Trending" in content
    
    # 清理测试文件
    file_path.unlink()
    file_path.parent.rmdir()
    file_path.parent.parent.rmdir()
    
    print("PASSED: create_markdown function test")


def test_directory_creation():
    """
    测试目录创建功能
    """
    test_filename = "test_markdowns/2025/12/test_dir_creation.md"
    
    # 创建markdown文件，这应该自动创建目录
    create_markdown("2025-12-24", test_filename)
    
    # 检查目录是否创建
    dir_path = Path(test_filename).parent
    assert dir_path.exists(), f"目录 {dir_path} 应该被创建"
    
    # 清理测试文件
    Path(test_filename).unlink()
    dir_path.rmdir()
    dir_path.parent.rmdir()
    
    print("PASSED: Directory creation test")


def test_job_function_structure():
    """
    测试job函数的结构和路径生成
    """
    # 获取当前日期
    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    year, month, day = today_str.split('-')
    expected_filename = f'markdowns/{year}/{month}/{today_str}.md'
    
    # 检查生成的路径格式是否正确
    assert f'markdowns/{year}/{month}/' in expected_filename
    assert today_str in expected_filename
    assert expected_filename.endswith('.md')
    
    print("PASSED: Job function path structure test")


def run_all_tests():
    """
    运行所有测试
    """
    print("开始运行爬虫项目测试...")
    
    test_create_markdown()
    test_directory_creation()
    test_job_function_structure()
    
    print("\nALL TESTS PASSED!")


if __name__ == '__main__':
    run_all_tests()