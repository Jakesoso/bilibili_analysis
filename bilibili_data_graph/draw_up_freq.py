from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd

font = {'family': 'SimSun',
        'size': '25'}
plt.rc('font', **font)
plt.rc('axes', unicode_minus=False)


def get_uploader_list():
    # 多个 Excel 文件路径
    file_paths = ['../data/rank_list.xlsx', '../data/weekly_list.xlsx']

    # 存储所有作者的计数器
    author_counter = Counter()

    # 遍历多个 Excel 文件
    for file_path in file_paths:
        # 读取 Excel 文件
        excel_file = pd.ExcelFile(file_path)

        # 遍历所有工作表
        for sheet_name in excel_file.sheet_names:
            # 读取工作表数据
            df = excel_file.parse(sheet_name)

            # 统计作者的出现次数
            authors = df['author'].tolist()
            author_counter.update(authors)

    # 提取前20个出现次数最多的作者
    top_authors = author_counter.most_common(20)

    # # 打印结果
    # for author, count in top_authors:
    #     print(author, count)
    return top_authors


def draw_up_freq():
    # 解析作者和出现次数
    top_authors = get_uploader_list()
    authors, counts = zip(*top_authors)

    # 创建一个指定大小的图表
    fig, ax = plt.subplots(figsize=(15, 10))

    # 创建柱状图
    ax.bar(authors, counts)

    # 设置图表标题和轴标签
    ax.set_title('Top 20 Authors')
    ax.set_xlabel('Author')
    ax.set_ylabel('Count')

    plt.subplots_adjust(top=0.9, bottom=0.4)

    # 旋转 x 轴标签以避免重叠
    plt.xticks(rotation=90)

    # 显示图表
    plt.show()
