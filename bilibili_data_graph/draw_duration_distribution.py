from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd

font = {'family': 'SimSun',
        'size': '25'}
plt.rc('font', **font)
plt.rc('axes', unicode_minus=False)


# 获取时长变化图/趋势
def get_durations_trend_list():
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

        # 统计时长的出现次数
        durations = df['duration'].tolist()
        for duration in durations:
            if 0 < duration < 30:
                year_counters[year].update(["<30s"])
            elif 30 <= duration < 3 * 60:
                year_counters[year].update(["30s-3min"])
            elif 3 * 60 <= duration < 5 * 60:
                year_counters[year].update(["3min-5min"])
            elif 5 * 60 <= duration < 15 * 60:
                year_counters[year].update(["5min-15min"])
            elif 15 * 60 <= duration < 30 * 60:
                year_counters[year].update(["15min-30min"])
            elif 30 * 60 <= duration < 45 * 60:
                year_counters[year].update(["30min-45min"])
            else:
                year_counters[year].update([">45min"])

    # 计算占比
    yearly_duration_ratios = {}
    for year, counter in year_counters.items():
        total_count = sum(counter.values())
        duration_ratios = [(duration, count / total_count) for duration, count in counter.items()]
        yearly_duration_ratios[year] = duration_ratios

    return yearly_duration_ratios


def get_video_duration_list():
    # 多个 Excel 文件路径
    file_paths = ['../data/rank_list.xlsx', '../data/weekly_list.xlsx']
    durations = []

    # 遍历多个 Excel 文件
    for file_path in file_paths:
        # 读取 Excel 文件
        excel_file = pd.ExcelFile(file_path)
        # 遍历所有工作表
        for sheet_name in excel_file.sheet_names:
            # 读取工作表数据
            df = excel_file.parse(sheet_name)
            durations.extend(df['duration'])

    dur_counter = Counter()
    for duration in durations:
        if 0 < duration < 30:
            dur_counter.update(["<30s"])
        elif 30 <= duration < 3 * 60:
            dur_counter.update(["30s-3min"])
        elif 3 * 60 <= duration < 5 * 60:
            dur_counter.update(["3min-5min"])
        elif 5 * 60 <= duration < 15 * 60:
            dur_counter.update(["5min-15min"])
        elif 15 * 60 <= duration < 30 * 60:
            dur_counter.update(["15min-30min"])
        elif 30 * 60 <= duration < 45 * 60:
            dur_counter.update(["30min-45min"])
        else:
            dur_counter.update([">45min"])

    return dur_counter


# def draw_duration_freq():
#     durations = get_video_duration_list()
#
#     # custom order list
#     custom_order = ['<30s', '30s-3min', '3min-5min', '5min-15min', '15min-30min', '30min-45min', '>45min']
#
#     # Extract durations and counts from the dictionary
#     dur = list(durations.keys())
#     counts = list(durations.values())
#
#     # Sort dur and counts based on custom_order
#     dur_sorted, counts_sorted = zip(*sorted(zip(dur, counts), key=lambda x: custom_order.index(x[0])))
#
#     # Create a figure object and specify the size
#     fig, ax = plt.subplots(figsize=(15, 7))
#
#     # Use plt.plot to draw a line plot
#     # plt.plot(dur_sorted, counts_sorted, marker='o', linestyle='-', linewidth=2)
#
#     # Use plt.bar to draw a bar chart
#     plt.bar(dur_sorted, counts_sorted)
#
#     # Set the chart title and axis labels
#     ax.set_title('Distribution of Video Durations')
#     ax.set_xlabel('Duration')
#     ax.set_ylabel('Count')
#
#     plt.subplots_adjust(top=0.8, bottom=0.4)
#
#     # Rotate x-axis labels for better visibility
#     # Manually set the x-axis tick positions and labels
#     plt.xticks(range(len(custom_order)), custom_order, rotation=45)
#
#     # Show the chart
#     plt.show()
#
#
# def draw_durations_trend():
#     yearly_duration_ratios = get_durations_trend_list()
#
#     years = sorted(yearly_duration_ratios.keys())
#
#     # 获取全部分区
#     categories = set()
#     for year in years:
#         top_categories = yearly_duration_ratios[year]
#         categories.update([category for category, count in top_categories])
#
#     # 保留在2023年出现次数最多的前10个分区
#     if '2023' in years:
#         top_categories_2023 = yearly_duration_ratios['2023']
#         top_categories_2023 = sorted(top_categories_2023, key=lambda x: x[1], reverse=True)
#         categories_2023 = [category for category, _ in top_categories_2023[:10]]
#         categories = categories.intersection(categories_2023)
#
#     plt.figure(figsize=(30, 20))  # 设置图形的大小
#
#     # 画图
#     for category in categories:
#         category_counts = [next((count for tag, count in yearly_duration_ratios[year] if tag == category), 0) for year
#                            in years]
#
#         plt.plot(years, category_counts, label=category, linewidth=3)
#
#         # 在每条线条旁边添加注记
#         last_count = category_counts[-1]
#         plt.text(years[-1], last_count, category, ha='left', va='center')
#
#     plt.xlabel('Year')  # 设置横轴标签
#     plt.ylabel('Percentage')  # 设置纵轴标签
#     plt.title('Duration Percentage Over Time')  # 设置图表标题
#     plt.legend(loc='upper left')  # 添加图例注记
#
#     plt.show()  # 显示图形
#

def draw_duration_dist():
    durations = get_video_duration_list()
    yearly_duration_ratios = get_durations_trend_list()

    # custom order list
    custom_order = ['<30s', '30s-3min', '3min-5min', '5min-15min', '15min-30min', '30min-45min', '>45min']

    # Extract durations and counts from the dictionary
    dur = list(durations.keys())
    counts = list(durations.values())

    # Sort dur and counts based on custom_order
    dur_sorted, counts_sorted = zip(*sorted(zip(dur, counts), key=lambda x: custom_order.index(x[0])))

    years = sorted(yearly_duration_ratios.keys())

    # 获取全部分区
    categories = set()
    for year in years:
        top_categories = yearly_duration_ratios[year]
        categories.update([category for category, count in top_categories])

    # 保留在2023年出现次数最多的前10个分区
    if '2023' in years:
        top_categories_2023 = yearly_duration_ratios['2023']
        top_categories_2023 = sorted(top_categories_2023, key=lambda x: x[1], reverse=True)
        categories_2023 = [category for category, _ in top_categories_2023[:10]]
        categories = categories.intersection(categories_2023)

    # 创建一个指定大小的图表
    fig, axs = plt.subplots(1, 2, figsize=(30, 20))

    # 绘制第一个表格 - 柱状图
    axs[0].bar(dur_sorted, counts_sorted)
    axs[0].set_title('Distribution of Video Durations')
    axs[0].set_xlabel('Duration')
    axs[0].set_ylabel('Count')
    axs[0].set_xticks(range(len(custom_order)))
    axs[0].set_xticklabels(custom_order, rotation=45)

    # 绘制第二个表格 - 折线图
    for category in categories:
        category_counts = [next((count for tag, count in yearly_duration_ratios[year] if tag == category), 0)
                           for year in years]
        axs[1].plot(years, category_counts, label=category, linewidth=3)
        last_count = category_counts[-1]
        axs[1].text(years[-1], last_count, category, ha='left', va='center')

    axs[1].set_xlabel('Year')
    axs[1].set_ylabel('Percentage')
    axs[1].set_title('Duration Percentage Over Time')
    axs[1].legend(loc='upper left')

    plt.tight_layout()  # 调整子图的布局
    plt.show()
