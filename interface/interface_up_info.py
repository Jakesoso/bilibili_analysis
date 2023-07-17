from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QDialog, QLineEdit, QHBoxLayout

from bilibili_data_graph import get_up_info


class UpInfoInter(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("指定UP主信息")
        self.resize(300, 300)
        self.layout = QVBoxLayout()

        # 第一行布局 文本框和确认按钮
        first_row_layout = QHBoxLayout()
        self.name_textbox = QLineEdit()
        self.confirm_button = QPushButton("确认")
        self.confirm_button.clicked.connect(self.get_info)
        first_row_layout.addWidget(QLabel("输入UP名字:"))
        first_row_layout.addWidget(self.name_textbox)
        first_row_layout.addWidget(self.confirm_button)
        self.layout.addLayout(first_row_layout)

        # 下方垂直布局 用于显示结果的标签和图像
        result_layout = QVBoxLayout()

        self.result_uid_label = QLabel()
        self.result_face_label = QLabel()
        self.result_image_label = QLabel()
        self.result_uid_label.setAlignment(Qt.AlignCenter)
        self.result_face_label.setAlignment(Qt.AlignCenter)
        self.result_image_label.setAlignment(Qt.AlignCenter)

        result_layout.addWidget(self.result_uid_label)
        result_layout.addWidget(self.result_face_label)
        result_layout.addWidget(self.result_image_label)
        self.layout.addLayout(result_layout)

        self.setLayout(self.layout)

    def get_info(self):
        # 获取文本框内容
        up_name = self.name_textbox.text()

        # 调用函数并传递参数
        result = get_up_info.get_up_info(up_name)

        # 解析返回值
        uid_value, face_img, up_freq_graph = result

        # 更新标签文本
        self.result_uid_label.setText(up_name + "的uid：" + str(uid_value))

        # 更新图像
        pixmap = QPixmap.fromImage(QImage.fromData(face_img))
        self.result_face_label.setPixmap(pixmap)

        # 显示up_freq_graph图像
        pixmap = QPixmap()
        pixmap.loadFromData(up_freq_graph.getvalue())
        self.result_image_label.setPixmap(pixmap)
