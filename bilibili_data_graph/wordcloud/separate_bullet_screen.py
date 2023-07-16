import glob
import os

import jieba

# 对弹幕进行分词操作
def bullet_screen_separate():
    # 读取要分析的文本
    bullet_screen_dir = "../data/weekly_list/"
    txt_files = glob.glob(os.path.join(bullet_screen_dir, '*combined_strings.txt'))

    for txt_file in txt_files:
        with open(txt_file, 'r', encoding="utf8") as file:
            content = file.read()
        seg_list = jieba.cut(content)
        seg_list = [word for word in seg_list if len(word) > 1]

        year = txt_file.split('_combined')[0]
        separate_dir = f"{year}_separate.txt"

        # 将分词结果写入文件
        with open(file=separate_dir, mode="w", encoding="utf-8") as f:
            f.write(" ".join(seg_list))

bullet_screen_separate()