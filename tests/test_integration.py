# -*- coding: utf-8 -*-
"""
集成测试
"""
import os
import sys
import tempfile
from pathlib import Path

# 添加项目根目录到Python路径，以便导入模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from crawler import create_markdown, save_to_md
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
            _extracted_from_test_full_workflow_14()
        finally:
            os.chdir(original_cwd)


# TODO Rename this here and in `test_full_workflow`
def _extracted_from_test_full_workflow_14():
    # 模拟创建测试目录
    test_markdowns_dir = Path("markdowns")
    test_markdowns_dir.mkdir(exist_ok=True)

    # 创建一个测试文件
    test_date = "2025-12-24"
    year, month, day = test_date.split("-")
    test_filename = f"markdowns/{year}/{month}/{test_date}.md"

    # 测试创建markdown文件
    create_markdown(test_date, test_filename)

    # 检查文件和目录是否正确创建
    file_path = Path(test_filename)
    assert file_path.exists(), f"文件 {test_filename} 应该被创建"

    # 检查内容是否正确
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert f"## {test_date} Github Trending" in content

    # 测试数据保存功能
    test_data = [
        ["test_project", "https://github.com/test/test", "A test project", 100, 20, 5],
        [
            "another_project",
            "https://github.com/another/test",
            "Another test project",
            200,
            30,
            10,
        ],
    ]

    save_to_md(test_data, test_filename, "python", topk=5)

    # 验证数据是否被追加到文件中
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "test_project" in content
        assert "another_project" in content
        assert "python" in content

    print("PASSED: 完整工作流程测试通过")


def test_history_organization_integration():
    """
    测试历史文件整理的集成
    """
    print("测试历史文件整理集成...")

    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        try:
            _extracted_from_test_history_organization_integration_13()
        finally:
            os.chdir(original_cwd)


# TODO Rename this here and in `test_history_organization_integration`
def _extracted_from_test_history_organization_integration_13():
    # 创建测试目录结构
    test_markdowns_dir = Path("markdowns")
    test_markdowns_dir.mkdir()

    # 创建一些测试历史文件
    (test_markdowns_dir / "2023-06-15.md").touch()
    (test_markdowns_dir / "2023-07-20.md").touch()
    (test_markdowns_dir / "2024-01-10.md").touch()
    (test_markdowns_dir / "2024-01-25.html").touch()
    (test_markdowns_dir / "readme.txt").touch()  # 非日期格式文件

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
    assert not (test_markdowns_dir / "2023-06-15.md").exists()
    assert not (test_markdowns_dir / "2023-07-20.md").exists()
    assert not (test_markdowns_dir / "2024-01-10.md").exists()
    assert not (test_markdowns_dir / "2024-01-25.html").exists()

    print("PASSED: 历史文件整理集成测试通过")


def test_path_generation():
    """
    测试路径生成逻辑
    """
    print("测试路径生成逻辑...")

    # 测试不同日期的路径生成
    def generate_expected_path(date_str):
        year, month, day = date_str.split("-")
        return f"markdowns/{year}/{month}/{date_str}.md"

    # Case 1
    date_str1, expected_path1 = "2024-01-01", "markdowns/2024/01/2024-01-01.md"
    generated_path1 = generate_expected_path(date_str1)
    assert (
        generated_path1 == expected_path1
    ), f"路径生成错误: 期望 {expected_path1}, 得到 {generated_path1}"

    # Case 2
    date_str2, expected_path2 = "2024-12-31", "markdowns/2024/12/2024-12-31.md"
    generated_path2 = generate_expected_path(date_str2)
    assert (
        generated_path2 == expected_path2
    ), f"路径生成错误: 期望 {expected_path2}, 得到 {generated_path2}"

    # Case 3
    date_str3, expected_path3 = "2025-02-28", "markdowns/2025/02/2025-02-28.md"
    generated_path3 = generate_expected_path(date_str3)
    assert (
        generated_path3 == expected_path3
    ), f"路径生成错误: 期望 {expected_path3}, 得到 {generated_path3}"

    # Case 4
    date_str4, expected_path4 = "2025-11-15", "markdowns/2025/11/2025-11-15.md"
    generated_path4 = generate_expected_path(date_str4)
    assert (
        generated_path4 == expected_path4
    ), f"路径生成错误: 期望 {expected_path4}, 得到 {generated_path4}"

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


if __name__ == "__main__":
    run_all_tests()
