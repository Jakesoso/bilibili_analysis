import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

font = {'family': 'SimSun',
        'size': '25'}
plt.rc('font', **font)
plt.rc('axes', unicode_minus=False)


# 分区上榜情况
def get_categories_list():
    # 多个 Excel 文件路径
    file_paths = ['../data/rank_list.xlsx', '../data/weekly_list.xlsx']

    # 存储所有分区的计数器
    category_counter = Counter()

    # 遍历多个 Excel 文件
    for file_path in file_paths:
        # 读取 Excel 文件
        excel_file = pd.ExcelFile(file_path)

        # 遍历所有工作表
        for sheet_name in excel_file.sheet_names:
            # 读取工作表数据
            df = excel_file.parse(sheet_name)

            # 统计分区的出现次数
            categories = df['tag'].tolist()
            category_counter.update(categories)

    # 提取前20个出现次数最多的tag
    top_category = category_counter.most_common(30)

    # # 打印结果
    # for author, count in top_authors:
    #     print(author, count)
    return top_category


# 获取分区热度变化图/趋势
def get_categories_trend_list():
    file_path = '../data/weekly_list.xlsx'
    year_counters = {}

    excel_file = pd.ExcelFile(file_path)

    for sheet_name in excel_file.sheet_names:
        df = excel_file.parse(sheet_name)

        # 提取年份
        year = sheet_name.split('第')[0].strip()

        # 检查是否已存在该年份的计数器
        if year not in year_counters:
            year_counters[year] = Counter()

        # 统计分区的出现次数
        categories = df['tag'].tolist()
        year_counters[year].update(categories)

    # 计算占比
    yearly_category_ratios = {}
    for year, counter in year_counters.items():
        total_count = sum(counter.values())
        category_ratios = [(category, count / total_count) for category, count in counter.items()]
        yearly_category_ratios[year] = category_ratios

    return yearly_category_ratios


# def draw_category_freq():
#     # 解析分区和出现次数
#     top_categories = get_categories_list()
#     cate, counts = zip(*top_categories)
#
#     # 创建一个指定大小的图表
#     fig, ax = plt.subplots(figsize=(25, 15))
#
#     # 创建柱状图
#     ax.bar(cate, counts)
#
#     # 设置图表标题和轴标签
#     ax.set_title('Top 30 Tags')
#     ax.set_xlabel('Tags')
#     ax.set_ylabel('Count')
#
#     plt.subplots_adjust(top=0.9, bottom=0.3)
#
#     # 旋转 x 轴标签以避免重叠
#     plt.xticks(rotation=90)
#
#     # 显示图表
#     plt.show()
#
#
# # 舍去在2023年未出现过的分区
# def draw_categories_trend():
#     yearly_top_categories = get_categories_trend_list()
#
#     years = sorted(yearly_top_categories.keys())
#
#     # 获取全部分区
#     categories = set()
#     for year in years:
#         top_categories = yearly_top_categories[year]
#         categories.update([category for category, count in top_categories])
#
#     # 保留在2023年出现次数最多的前10个分区
#     if '2023' in years:
#         top_categories_2023 = yearly_top_categories['2023']
#         top_categories_2023 = sorted(top_categories_2023, key=lambda x: x[1], reverse=True)
#         categories_2023 = [category for category, _ in top_categories_2023[:10]]
#         categories = categories.intersection(categories_2023)
#
#     plt.figure(figsize=(30, 20))  # 设置图形的大小
#
#     # 画图
#     for category in categories:
#         category_counts = [next((count for tag, count in yearly_top_categories[year] if tag == category), 0)
#                            for year in years]
#
#         plt.plot(years, category_counts, label=category, linewidth=3)
#
#         # 在每条线条旁边添加注记
#         last_count = category_counts[-1]
#         plt.text(years[-1], last_count, category, ha='left', va='center', fontsize=15)
#
#     plt.xlabel('Year')  # 设置横轴标签
#     plt.ylabel('Percentage')  # 设置纵轴标签
#     plt.title('Category Percentage Over Time')  # 设置图表标题
#     plt.legend(loc='upper left')  # 添加图例注记
#
#     plt.show()  # 显示图形


def draw_category_dist():
    # 解析分区和出现次数
    top_categories = get_categories_list()
    cate, counts = zip(*top_categories)

    # 创建一个指定大小的图表
    fig, axs = plt.subplots(1, 2, figsize=(30, 20))

    # 绘制第一个表格 - 柱状图
    axs[0].bar(cate, counts)
    axs[0].set_title('Top 30 Categories')
    axs[0].set_xlabel('Categories')
    axs[0].set_ylabel('Count')
    axs[0].set_xticklabels(cate, rotation=90)

    # 绘制第二个表格 - 折线图
    yearly_top_categories = get_categories_trend_list()
    years = sorted(yearly_top_categories.keys())
    categories = set()
    for year in years:
        top_categories = yearly_top_categories[year]
        categories.update([category for category, count in top_categories])
    if '2023' in years:
        top_categories_2023 = yearly_top_categories['2023']
        top_categories_2023 = sorted(top_categories_2023, key=lambda x: x[1], reverse=True)
        categories_2023 = [category for category, _ in top_categories_2023[:10]]
        categories = categories.intersection(categories_2023)
    for category in categories:
        category_counts = [next((count for tag, count in yearly_top_categories[year] if tag == category), 0)
                           for year in years]
        axs[1].plot(years, category_counts, label=category, linewidth=3)
        last_count = category_counts[-1]
        axs[1].text(years[-1], last_count, category, ha='left', va='center', fontsize=15)

    axs[1].set_xlabel('Year')
    axs[1].set_ylabel('Percentage')
    axs[1].set_title('Category Percentage Over Time')
    axs[1].legend(loc='upper left')

    plt.tight_layout()  # 调整子图的布局
    plt.show()
