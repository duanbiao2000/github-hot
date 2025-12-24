# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description:
"""
import os
import re
from pathlib import Path


def organize_history_files():  # sourcery skip: use-getitem-for-re-match-groups
    """
    将markdowns目录下的历史文件按年/月进行归类
    """
    markdowns_dir = Path("markdowns")

    # 遍历markdowns目录下的所有文件
    for file_path in markdowns_dir.iterdir():
        # 检查是否为.md或.html文件
        if file_path.is_file() and file_path.suffix in [".md", ".html"]:
            if match := re.match(r"(\d{4})-(\d{2})-\d{2}", file_path.stem):
                year = match.group(1)
                month = match.group(2)

                # 创建年/月子目录
                year_month_dir = markdowns_dir / year / month
                year_month_dir.mkdir(parents=True, exist_ok=True)

                # 移动文件到相应的年/月目录
                new_path = year_month_dir / file_path.name
                file_path.rename(new_path)
                print(f"Moved {file_path.name} to {new_path}")
            else:
                # 如果文件名不包含日期格式，则跳过
                print(f"Skipped {file_path.name} - does not match date format")


if __name__ == "__main__":
    organize_history_files()
    print("History files organization completed.")
