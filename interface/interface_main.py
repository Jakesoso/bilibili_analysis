import subprocess
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

from interface_wordcloud import WordcloudInter
from interface_up_info import UpInfoInter

from bilibili_data_graph import draw_up_freq
from bilibili_data_graph import draw_category_distribution
from bilibili_data_graph import draw_duration_distribution
from bilibili_data_graph import draw_pubtime_distribution


class BilibiliDataAnalysis(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle("哔哩哔哩数据分析")
        self.resize(300, 300)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建并添加软件名称标签
        label_title = QLabel("哔哩哔哩数据分析")
        label_title.setAlignment(Qt.AlignCenter)

        # 添加爬取信息部分分隔标签
        label_separator1 = QLabel("----------爬取信息部分----------")
        label_separator1.setAlignment(Qt.AlignCenter)

        # 添加数据分析部分分隔标签
        label_separator2 = QLabel("----------数据分析部分----------")
        label_separator2.setAlignment(Qt.AlignCenter)

        # 创建爬取信息部分按钮
        btn_crawl_ranking = QPushButton("爬取排行榜信息")
        btn_crawl_ranking.clicked.connect(self.scraping_ranking_list)

        btn_crawl_weekly = QPushButton("爬取周榜信息")
        btn_crawl_weekly.clicked.connect(self.scraping_ranking_list)

        # 创建数据分析部分按钮
        btn_wordcloud = QPushButton("每年弹幕词云图")
        btn_wordcloud.clicked.connect(self.gen_wordcloud)

        btn_up_ranking = QPushButton("Up上榜情况")
        btn_up_ranking.clicked.connect(draw_up_freq.draw_up_freq)

        btn_crawl_up_info = QPushButton("分析指定UP主信息")
        btn_crawl_up_info.clicked.connect(self.get_up_info)

        btn_duration_distribution = QPushButton("上榜视频时长分布")
        btn_duration_distribution.clicked.connect(draw_duration_distribution.draw_duration_dist)

        btn_category_distribution = QPushButton("上榜视频分区分布")
        btn_category_distribution.clicked.connect(draw_category_distribution.draw_category_dist)

        btn_publish_time_distribution = QPushButton("上榜视频发布时间分布")
        btn_publish_time_distribution.clicked.connect(draw_pubtime_distribution.draw_publtime_dist)

        # 添加按钮到布局
        layout.addWidget(label_title)

        layout.addWidget(label_separator1)

        layout.addWidget(btn_crawl_ranking)
        layout.addWidget(btn_crawl_weekly)

        layout.addWidget(label_separator2)
        layout.addWidget(btn_wordcloud)
        layout.addWidget(btn_crawl_up_info)
        layout.addWidget(btn_up_ranking)
        layout.addWidget(btn_duration_distribution)
        layout.addWidget(btn_category_distribution)
        layout.addWidget(btn_publish_time_distribution)

        # 设置布局到窗口
        self.setLayout(layout)

        # 显示窗口
        self.show()

    def scraping_ranking_list(self):
        # 替换为您的Scrapy项目所在的文件夹路径
        scrapy_project_path = '../bilibili_scrapy/bilibili_scrapy'

        # 替换为您的Scrapy爬虫名称
        spider_name = 'bilibili_spider'

        # 在指定文件夹中启动Scrapy命令
        subprocess.Popen(['scrapy', 'crawl', spider_name], cwd=scrapy_project_path)

    def gen_wordcloud(self):
        dialog = WordcloudInter()
        dialog.exec_()

    def get_up_info(self):
        dialog = UpInfoInter()
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BilibiliDataAnalysis()
    sys.exit(app.exec_())
