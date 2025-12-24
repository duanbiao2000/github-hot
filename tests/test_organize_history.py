# -*- coding: utf-8 -*-
"""
测试历史文件整理功能
"""
import os
import sys
import tempfile
from pathlib import Path

# 添加项目根目录到Python路径，以便导入模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.organize_history import organize_history_files


def test_organize_history_files():
    """
    测试历史文件整理功能
    """
    # 创建临时目录进行测试
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建测试目录结构
        test_markdowns_dir = Path(temp_dir) / "markdowns"
        test_markdowns_dir.mkdir()
        
        # 创建一些测试文件
        test_files = [
            "2024-01-01.md",
            "2024-01-15.md", 
            "2024-02-01.md",
            "2024-12-31.md",
            "some_random_file.txt",  # 这个不应该被移动
            "2025-03-10.md",
            "2025-03-10.html"  # 测试HTML文件
        ]
        
        for filename in test_files:
            (test_markdowns_dir / filename).touch()
        
        # 运行组织历史文件的函数
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        try:
            organize_history_files()
        finally:
            os.chdir(original_cwd)
        
        # 验证文件是否被正确移动
        expected_locations = {
            "2024-01-01.md": test_markdowns_dir / "2024" / "01" / "2024-01-01.md",
            "2024-01-15.md": test_markdowns_dir / "2024" / "01" / "2024-01-15.md",
            "2024-02-01.md": test_markdowns_dir / "2024" / "02" / "2024-02-01.md",
            "2024-12-31.md": test_markdowns_dir / "2024" / "12" / "2024-12-31.md",
            "2025-03-10.md": test_markdowns_dir / "2025" / "03" / "2025-03-10.md",
            "2025-03-10.html": test_markdowns_dir / "2025" / "03" / "2025-03-10.html"
        }
        
        # 检查日期格式的文件是否被移动到正确位置
        for original_filename, expected_path in expected_locations.items():
            assert expected_path.exists(), f"文件 {expected_path} 应该存在"
            assert not (test_markdowns_dir / original_filename).exists(), f"原文件 {original_filename} 应该已被移动"
        
        # 检查非日期格式的文件是否未被移动
        assert (test_markdowns_dir / "some_random_file.txt").exists(), "非日期格式文件应该保持原位"
        
        # 检查目录结构
        assert (test_markdowns_dir / "2024" / "01").exists(), "2024年1月目录应该被创建"
        assert (test_markdowns_dir / "2024" / "02").exists(), "2024年2月目录应该被创建"
        assert (test_markdowns_dir / "2024" / "12").exists(), "2024年12月目录应该被创建"
        assert (test_markdowns_dir / "2025" / "03").exists(), "2025年3月目录应该被创建"
        
        print("PASSED: 历史文件整理功能测试通过")


def run_all_tests():
    """
    运行所有测试
    """
    print("开始运行历史文件整理功能测试...")
    test_organize_history_files()
    print("\nALL TESTS PASSED!")


if __name__ == '__main__':
    run_all_tests()