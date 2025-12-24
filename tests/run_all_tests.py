# -*- coding: utf-8 -*-
"""
运行所有测试
"""
import subprocess
import sys
import os


def run_test(test_file):
    """
    运行单个测试文件
    """
    print(f"\n{'='*50}")
    print(f"运行测试: {test_file}")
    print(f"{'='*50}")
    
    # 构建完整的测试文件路径
    full_path = os.path.join("tests", test_file)
    result = subprocess.run([sys.executable, full_path], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ {test_file} 测试通过")
    else:
        print(f"✗ {test_file} 测试失败")
        print("错误输出:")
        print(result.stderr)
    
    print(result.stdout)
    return result.returncode == 0


def main():
    """
    主函数，运行所有测试
    """
    print("开始运行所有测试...")
    
    test_files = [
        "test_crawler.py",
        "test_organize_history.py", 
        "test_integration.py"
    ]
    
    all_passed = True
    
    for test_file in test_files:
        if not run_test(test_file):
            all_passed = False
    
    print(f"\n{'='*50}")
    if all_passed:
        print("🎉 所有测试都通过了！")
    else:
        print("❌ 有些测试失败了")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()