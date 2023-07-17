import glob
import os
import re


# 合并一年的弹幕 并且只保留文字

def combine_bullet_screen():
    # 弹幕文件
    bullet_screen_dir = "../data/weekly_list/"

    # 获取所有文件夹
    folders = glob.glob(os.path.join(bullet_screen_dir, '*第*期*'))

    # 创建一个字典，用于按年份分类存储字符串
    yearly_strings = {}

    # 遍历文件夹
    for folder in folders:
        # 解析文件夹名字获取年份
        year = folder.split('第')[0]

        # 获取文件夹中所有txt文件
        txt_files = glob.glob(os.path.join(folder, '*.txt'))

        # 创建一个列表，用于存储当前文件夹内的所有字符串
        folder_strings = []

        # 遍历txt文件
        for txt_file in txt_files:
            # 读取txt文件内容
            with open(txt_file, 'r', encoding='utf-8') as file:
                content = file.read()

                # 解析txt文件内容获取bulletScreen里的字符串
                bulletScreen = eval(content)['bulletScreen']

                # 将bulletScreen的字符串添加到列表中
                folder_strings.extend(bulletScreen)

        # 将当前文件夹内的所有字符串合并成一个大的字符串
        combined_string = ' '.join(folder_strings)

        # 只保留文字
        filtered_content = re.sub('[^\u4e00-\u9fa5]+', '', combined_string)

        # 将大的字符串添加到对应年份的字典中
        if year in yearly_strings:
            yearly_strings[year] += filtered_content
        else:
            yearly_strings[year] = filtered_content

    # 将每个年份的字符串存储到一个文件中
    for year, string in yearly_strings.items():
        with open(f'{year}_combined_strings.txt', 'w', encoding='utf-8') as file:
            file.write(string)


combine_bullet_screen()
