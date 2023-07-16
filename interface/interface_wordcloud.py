import subprocess
import sys
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QDialog


class WordcloudInter(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("绘制弹幕词云图")

        self.resize(300, 300)
        self.layout = QVBoxLayout()

        btn_combine_bs = QPushButton("合并弹幕信息")
        btn_combine_bs.clicked.connect(partial(self.run_script, 'combine_bullet_screen.py'))

        btn_separate_bs = QPushButton("弹幕分词")
        btn_separate_bs.clicked.connect(partial(self.run_script, 'separate_bullet_screen.py'))

        btn_gen_bs = QPushButton("生成词云图")
        btn_gen_bs.clicked.connect(partial(self.run_script, 'generate_wordcloud.py'))

        self.layout.addWidget(QLabel("词云图").setAlignment(Qt.AlignCenter))
        self.layout.addWidget(btn_combine_bs)
        self.layout.addWidget(btn_separate_bs)
        self.layout.addWidget(btn_gen_bs)

        self.setLayout(self.layout)

    def run_script(self, script):
        # 替换为您要运行的Python脚本的文件路径
        script_path = '../bilibili_data_graph/wordcloud/'

        # 在子进程中运行Python脚本
        subprocess.Popen([sys.executable, script_path + script])
