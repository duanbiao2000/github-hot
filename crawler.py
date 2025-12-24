# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description:
"""
import datetime
import os
from codecs import open

import pandas as pd
import requests
from pyquery import PyQuery
import pathlib


def git_add_commit_push(date, filename):
    """
    执行git添加、提交和推送操作。

    该函数通过给定的日期和文件名，执行git add、commit和push操作。
    使用os.system()函数来执行git命令，将文件添加到版本控制，然后提交并推送到远程仓库。

    参数:
    date (str): 提交时的日期，用于提交信息。
    filename (str): 需要添加和提交的文件名。

    返回值:
    无返回值，但会依次执行git add、git commit和git push命令。
    """
    # 构造git add命令，将指定文件添加到暂存区
    cmd_git_add = "git add {filename}".format(filename=filename)
    # 构造git commit命令，使用给定的日期作为提交信息
    cmd_git_commit = 'git commit -m "{date}"'.format(date=date)
    # 构造git push命令，推送到远程仓库的master分支
    cmd_git_push = "git push -u origin master"

    # 执行git add命令
    os.system(cmd_git_add)
    # 执行git commit命令
    os.system(cmd_git_commit)
    # 执行git push命令
    os.system(cmd_git_push)


def create_markdown(date, filename):
    """
    创建一个Markdown文件，并写入指定日期的标题。

    :param date: 日期字符串，用于生成文件标题。
    :param filename: 文件名字符串，指定要创建的Markdown文件的名称。
    """
    # 创建目录路径（如果不存在）
    pathlib.Path(filename).parent.mkdir(parents=True, exist_ok=True)

    # 使用with语句创建或打开一个名为filename的文件，以写入模式，并指定编码为utf-8
    with open(filename, "w", encoding="utf-8") as f:
        # 写入Markdown文件的标题，包含日期的标题信息
        f.write("## " + date + " Github Trending\n")


def scrape(language, filename, topk=5):
    """
    根据给定的编程语言获取GitHub上的热门项目，并将结果保存到Markdown文件中。

    参数:
    - language: str, 编程语言名称，用于访问GitHub趋势页面。
    - filename: str, 保存结果的Markdown文件名。
    - topk: int, 保存到文件的热门项目数量，默认为5。

    该函数首先设置请求头来模拟浏览器行为，然后根据指定的编程语言获取GitHub trending页面的内容。
    使用PyQuery解析HTML，提取每个项目的标题、描述、URL、星星数、fork数以及新星数。
    最后，将收集的数据保存到指定的Markdown文件中，只保存指定数量的顶级热门项目。
    """
    # 设置请求头，以绕过可能的爬虫检测
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
    }

    # 构造GitHub趋势页面的URL
    url = "https://github.com/trending/{language}".format(language=language)
    # 发起GET请求获取页面内容
    r = requests.get(url, headers=HEADERS)
    # 确保请求成功
    assert r.status_code == 200

    # 使用PyQuery解析页面内容
    d = PyQuery(r.content)
    # 获取页面上所有项目的元素
    items = d("div.Box article.Box-row")
    ds = []
    for item in items:
        # 对每个项目元素进行详细解析
        i = PyQuery(item)
        title = i(".lh-condensed a").text()
        description = i("p.col-9").text()
        url = i(".lh-condensed a").attr("href")
        url = "https://github.com" + url
        star_fork = i(".f6 a").text().strip()
        star, fork = star_fork.split()
        # 从页面元素中提取新的星数
        # 这里使用了链式调用，首先通过类名".f6 svg.octicon-star"定位到星数图标
        # 然后通过parent()方法找到其父元素，调用.text()方法获取父元素的文本内容
        # .strip()用于去除首尾空白字符，split()[1]则是将文本按空格分割后取第二个元素，即新的星数
        new_star = i(".f6 svg.octicon-star").parent().text().strip().split()[1]
        star = int(star.replace(",", ""))
        fork = int(fork.replace(",", ""))
        new_star = int(new_star.replace(",", ""))
        ds.append([title, url, description, star, fork, new_star])
    # 将收集的数据保存到Markdown文件中
    save_to_md(ds, filename, language, topk)


def save_to_md(ds, filename, language, topk=5):
    """
    将数据集保存为Markdown格式文件。

    本函数通过以下步骤处理数据并保存到Markdown文件中：
    1. 将数据集转换为DataFrame；
    2. 根据新的星标数、总星标数和fork数对DataFrame进行排序；
    3. 重置索引并选择排名前topk的项目；
    4. 将筛选后的数据以Markdown格式写入指定文件。

    参数:
    - ds: 数据集，通常是一个列表，包含项目的信息；
    - filename: 要保存的文件名；
    - language: 语言名称，用于在文件中标识部分；
    - topk: 要保存的顶级项目数量，默认为5。

    返回值:
    无
    """
    # 将数据集转换为DataFrame，并进行排序和筛选
    df = pd.DataFrame(
        ds, columns=["title", "url", "description", "star", "fork", "new_star"]
    )
    df.sort_values(by=["new_star", "star", "fork"], ascending=False, inplace=True)
    # 重置数据框(df)的索引，以确保索引连续且与数据行一一对应
    df.reset_index(drop=True, inplace=True)
    df = df.head(topk)

    # 打开文件并写入数据
    with open(filename, "a", "utf-8") as f:
        # 在文件中添加语言标识
        f.write("\n### {language}\n".format(language=language))

        # 遍历DataFrame，将每个项目的信息写入文件
        for i in range(len(df)):
            # 通过iloc方法获取DataFrame中第i行的'title'字段值
            title = df.iloc[i]["title"]
            url = df.iloc[i]["url"]
            description = df.iloc[i]["description"]
            star = df.iloc[i]["star"]
            fork = df.iloc[i]["fork"]
            new_star = df.iloc[i]["new_star"]

            # 构造项目信息的Markdown格式字符串
            out = "* [{title}]({url}): {description} ***Star:{stars} Fork:{fork} Today stars:{new_star}***\n".format(
                title=title,
                url=url,
                description=description,
                stars=star,
                fork=fork,
                new_star=new_star,
            )
            # 将项目信息写入文件
            f.write(out)


def job():
    """
    主函数，用于执行整个抓取和生成Markdown文件的流程。
    该函数负责获取当前日期，生成对应的文件名，创建Markdown文件，
    抓取指定语言的 trending 信息到文件中，并输出保存文件的路径。
    """
    # 获取当前日期的字符串表示，格式为'YYYY-MM-DD'
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")

    # 从日期字符串中提取年份和月份，用于创建子目录结构
    year, month, day = today_str.split("-")

    # 根据当前日期生成Markdown文件的路径，按年/月创建子目录
    filename = f"markdowns/{year}/{month}/{today_str}.md"

    # 创建Markdown文件
    create_markdown(today_str, filename)

    # 开始抓取并写入Markdown文件
    # 首先抓取全网 trending 信息，然后分别抓取不同编程语言的 trending 信息
    scrape(
        "", filename, topk=10
    )  # full_url = 'https://github.com/trending?since=daily'
    scrape("python", filename)
    scrape("java", filename)
    scrape("javascript", filename)
    scrape("go", filename)
    # 输出Markdown文件保存的路径
    print("save markdown file to {filename}".format(filename=filename))

    # 将生成的Markdown文件添加到Git仓库并提交（注：此处缺少函数定义）
    # git_add_commit_push(strdate, filename)


if __name__ == "__main__":
    job()
