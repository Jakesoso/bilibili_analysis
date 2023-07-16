import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

font = {'family': 'SimSun',
        'size': '25'}
plt.rc('font', **font)
plt.rc('axes', unicode_minus=False)


# yearly_pub_week = {}
# yearly_pub_hour = {}
# for year, counter in yearly_pub_week_counters.items():
#     # 返回全部信息
#     yearly_pub_week[year] = counter.most_common(len(counter))
#
# for year, counter in yearly_pub_hour_counters.items():
#     # 返回全部信息
#     yearly_pub_hour[year] = counter.most_common(len(counter))

def get_publish_time_trend():
    file_path = '../data/weekly_list.xlsx'
    yearly_pub_week_counters = {}
    yearly_pub_hour_counters = {}

    excel_file = pd.ExcelFile(file_path)

    for sheet_name in excel_file.sheet_names:
        df = excel_file.parse(sheet_name)

        # 提取年份
        year = sheet_name.split('第')[0].strip()

        # 检查是否已存在
        if year not in yearly_pub_week_counters:
            yearly_pub_week_counters[year] = Counter()
        if year not in yearly_pub_hour_counters:
            yearly_pub_hour_counters[year] = Counter()

        # 将pubdate字段转换为周几
        weeks = pd.to_datetime(df['pubdate'], unit='s').dt.day_name().tolist()
        yearly_pub_week_counters[year].update(weeks)

        # 时间段
        hours = pd.to_datetime(df['pubdate'], unit='s').dt.hour.tolist()
        for hour in hours:
            if 1 <= hour < 5:
                yearly_pub_hour_counters[year].update(["凌晨"])
            elif 5 <= hour < 8:
                yearly_pub_hour_counters[year].update(["早上"])
            elif 8 <= hour < 11:
                yearly_pub_hour_counters[year].update(["上午"])
            elif 11 <= hour < 13:
                yearly_pub_hour_counters[year].update(["中午"])
            elif 13 <= hour < 17:
                yearly_pub_hour_counters[year].update(["下午"])
            elif 17 <= hour < 19:
                yearly_pub_hour_counters[year].update(["傍晚"])
            elif 19 <= hour < 23:
                yearly_pub_hour_counters[year].update(["晚上"])
            elif 23 <= hour < 1:
                yearly_pub_hour_counters[year].update(["子夜"])

    yearly_pub_week_ratios = {}
    yearly_pub_hour_ratios = {}
    for year, counter in yearly_pub_week_counters.items():
        total_count = sum(counter.values())
        duration_ratios = [(duration, count / total_count) for duration, count in counter.items()]
        yearly_pub_week_ratios[year] = duration_ratios

    for year, counter in yearly_pub_hour_counters.items():
        total_count = sum(counter.values())
        duration_ratios = [(duration, count / total_count) for duration, count in counter.items()]
        yearly_pub_hour_ratios[year] = duration_ratios

    return [yearly_pub_week_ratios, yearly_pub_hour_ratios]

# def draw_publish_time_freq():
#     # 读取Excel文件
#     df = pd.read_excel('../data/weekly_list.xlsx', sheet_name=None)
#
#     # 合并所有工作表的数据
#     merged_df = pd.concat(df.values(), ignore_index=True)
#
#     # 将pubdate字段转换为日期时间类型
#     merged_df['pubdate'] = pd.to_datetime(merged_df['pubdate'], unit='s')
#
#     # 绘制发布星期的柱形图
#     weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     weekday_counts = merged_df['pubdate'].dt.weekday.value_counts().reindex(range(7))
#     weekday_counts.index = weekday_names
#     plt.figure(figsize=(15, 15))
#     weekday_counts.plot(kind='bar', color='blue')
#     plt.xlabel('Weekday')
#     plt.ylabel('Count')
#     plt.title('Number of Videos Published by Weekday')
#     plt.xticks(rotation=45)  # 倾斜x轴标签
#     plt.show()
#
#     # 绘制发布时刻的柱形图
#     hour_counts = merged_df['pubdate'].dt.hour.value_counts().sort_index()
#     plt.figure(figsize=(8, 6))
#     hour_counts.plot(kind='bar', color='green')
#     plt.xlabel('Hour')
#     plt.ylabel('Count')
#     plt.title('Number of Videos Published by Hour')
#     plt.xticks(rotation=45, fontsize=18)  # 倾斜x轴标签
#     plt.show()
#
#
def draw_publish_time_trend():
    yearly_pub = get_publish_time_trend()

    for yearly_top_categories in yearly_pub:
        years = sorted(yearly_top_categories.keys())

        # 获取全部分区
        categories = set()
        for year in years:
            top_categories = yearly_top_categories[year]
            categories.update([category for category, count in top_categories])

        plt.figure(figsize=(30, 20))  # 设置图形的大小

        # 画图
        for category in categories:
            category_counts = [next((count for tag, count in yearly_top_categories[year] if tag == category), 0) for
                               year
                               in years]

            plt.plot(years, category_counts, label=category, linewidth=3)

            # 在每条线条旁边添加注记
            last_count = category_counts[-1]
            plt.text(years[-1], last_count, category, ha='left', va='center')

        plt.xlabel('Year')  # 设置横轴标签
        plt.ylabel('Percentage')  # 设置纵轴标签
        plt.title('Time Percentage Over Time')  # 设置图表标题
        plt.legend(loc='upper left')  # 添加图例注记

        plt.show()  # 显示图形


def draw_publtime_dist():
    # 读取Excel文件
    df = pd.read_excel('../data/weekly_list.xlsx', sheet_name=None)

    # 合并所有工作表的数据
    merged_df = pd.concat(df.values(), ignore_index=True)

    # 将pubdate字段转换为日期时间类型
    merged_df['pubdate'] = pd.to_datetime(merged_df['pubdate'], unit='s')

    # 绘制发布星期的柱形图
    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_counts = merged_df['pubdate'].dt.weekday.value_counts().reindex(range(7))

    # 绘制发布时刻的柱形图
    hour_counts = merged_df['pubdate'].dt.hour.value_counts().sort_index()

    # 创建一个具有适当布局的图表
    fig, axs = plt.subplots(2, 2, figsize=(25, 25))

    # 绘制第一个表格 - 星期柱形图
    axs[0, 0].bar(weekday_names, weekday_counts, color='blue')
    axs[0, 0].set_xlabel('Weekday')
    axs[0, 0].set_ylabel('Count')
    axs[0, 0].set_title('Number of Videos Published by Weekday')
    axs[0, 0].tick_params(axis='x', rotation=45)

    # 绘制第二个表格 - 时刻柱形图
    axs[0, 1].bar(hour_counts.index, hour_counts, color='green')
    axs[0, 1].set_xlabel('Hour')
    axs[0, 1].set_ylabel('Count')
    axs[0, 1].set_title('Number of Videos Published by Hour')
    axs[0, 1].tick_params(axis='x', rotation=45, labelsize=18)

    # 绘制第三四个表格 - 时间趋势图
    yearly_pub = get_publish_time_trend()

    k = 0
    for yearly_top_categories in yearly_pub:
        years = sorted(yearly_top_categories.keys())

        # 获取全部分区
        categories = set()
        for year in years:
            top_categories = yearly_top_categories[year]
            categories.update([category for category, count in top_categories])

        # 画图
        for category in categories:
            category_counts = [next((count for tag, count in yearly_top_categories[year] if tag == category), 0)
                               for year in years]

            axs[1, k].plot(years, category_counts, label=category, linewidth=3)

            # 在每条线条旁边添加注记
            last_count = category_counts[-1]
            axs[1, k].text(years[-1], last_count, category, ha='left', va='center')

        axs[1, k].set_xlabel('Year')
        axs[1, k].set_ylabel('Percentage')
        axs[1, k].set_title('Time Percentage Over Time')
        axs[1, k].legend(loc='upper left')
        k = k + 1

    # 调整子图间距
    plt.subplots_adjust(hspace=0.5, wspace=0.3)

    # 显示图表
    plt.show()
