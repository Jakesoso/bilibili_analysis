# 生成词云

import glob
import os

import numpy as np
import wordcloud
from PIL import Image

# stopwords_custom = {'真的', '哈哈哈', '哈哈哈哈', '啊啊啊', '了', '一', '有', '我', '是', '这', '不', '就', '的', '或',
#                     '个'}
stopwords_custom = {'真的', '哈哈哈', '哈哈哈哈', '啊啊啊', '了', '一', '有', '我', '是', '这', '不', '就', '的', '或', '个',
                    '感觉', '喜欢', '老师', '厉害', '好听', '好看', '世界', '视频', '好像', '呜呜', '哔哩', '弹幕', '两个', '这是'}

'''
停用词来源：https://blog.csdn.net/qq_33772192/article/details/91886847
'''

stopwords = set()
content = [sw_c for sw_c in stopwords_custom] + [line.strip() for line in open('./stopwords.txt', 'r').readlines()]
stopwords.update(content)

bullet_screen_dir = "../../data/weekly_list/"
mask_img = Image.open("b_cover.png")
txt_files = glob.glob(os.path.join(bullet_screen_dir, '*separate.txt'))

for txt_file in txt_files:
    with open(txt_file, 'r', encoding="utf8") as file:
        content = file.read()

    # 生成
    wc = wordcloud.WordCloud(
        background_color="white",
        # width=1000,
        # height=1000,
        collocations=False,
        # max_words=200,
        mask=np.array(mask_img),
        # max_font_size=60,
        # random_state=42,
        font_path='C:/Windows/Fonts/simsun.ttc',  # 中文处理，用系统自带的字体
        stopwords=stopwords
    ).generate(content)

    # # 获取词云中的词频
    # word_frequencies = wc.process_text(content)

    # # 对词频进行排序
    # sorted_word_frequencies = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)

    # # 在终端输出词云图上词频最大的30个词
    # for word, frequency in sorted_word_frequencies[:30]:
    #     print(f"{word}")

    year = txt_file.split('_separate')[0]

    # 保存云图
    wc.to_file(f"{year}_wordcloud.png")

    print("----------------------------------")
