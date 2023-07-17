import io

import matplotlib.pyplot as plt
import pandas as pd
import requests

font = {'family': 'SimSun',
        'size': '25'}
plt.rc('font', **font)
plt.rc('axes', unicode_minus=False)


def draw_sp_up_freq(up_name):
    file_path = '../data/weekly_list.xlsx'
    year_counters = {}

    excel_file = pd.ExcelFile(file_path)

    for sheet_name in excel_file.sheet_names:
        df = excel_file.parse(sheet_name)

        # 提取年份
        year = sheet_name.split('第')[0].strip()

        # 检查是否已存在该年份的计数器
        if year not in year_counters:
            year_counters[year] = 0

        # 统计某一位up主的出现次数
        uploader_occurrences = df[df['up_name'] == up_name]
        count = len(uploader_occurrences)
        year_counters[year] += count

    years = sorted(year_counters.keys())
    counts = [year_counters[year] for year in years]

    plt.figure(figsize=(10, 8))
    plt.plot(years, counts, marker='o', linestyle='-', linewidth=2)

    plt.xlabel('Year')
    plt.ylabel('Occurrences')
    plt.title(f'Occurrences of Uploader "{up_name}" Over Time')

    return plt


def get_up_info(up_name):
    # 读取Excel文件
    df = pd.read_excel('../data/weekly_list.xlsx', sheet_name=None)

    # 合并所有工作表的数据
    merged_df = pd.concat(df.values(), ignore_index=True)

    # 使用条件筛选
    filtered_data = merged_df[merged_df['up_name'] == up_name].iloc[0]

    # 获取筛选后的数据的不同字段的值
    uid_value = filtered_data['up_mid']
    face_value = filtered_data['up_face']
    up_freq_plt = draw_sp_up_freq(up_name)

    # 将图形保存为内存中的图像对象
    up_freq_graph = io.BytesIO()
    up_freq_plt.savefig(up_freq_graph, format='png')
    up_freq_graph.seek(0)

    face_img = requests.get(face_value).content

    return [uid_value, face_img, up_freq_graph]
