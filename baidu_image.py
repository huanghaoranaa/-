# -*- coding:utf-8 -*-
# @author Python 集中营
# @date 2022/1/24
# @file test8.py

# done

# 百度图片下载器2.0

# 前段时间写了一个百度图片下载器，结果发现有很多人需要使用。说实话之前写的那一款百度图片下载器比较LOW，今天刚好有时间就做了一下升级。

# 更新了两个BUG，一个是图片下载达到几千张的时候就没有图片可以下载了。另一个是下载进度不能实时的展示出来不知道下载到什么程度了。

# 图：百度图片下载器2.0.png

# 同样的，我们先把需要的第三方库导入进来。

'''UI界面相关的库'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

'''应用操作相关的库'''
import sys
import os

from scripy_images import ScripyImages


class baiduImage(QWidget):
    def __init__(self):
        super(baiduImage, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('百度图片下载器2.0  公众号：[Python 集中营]')
        self.setWindowIcon(QIcon('下载.ico'))
        self.setFixedSize(550, 300)

        grid = QGridLayout()

        self.page_label = QLabel()
        self.page_label.setText('设置爬取页数：')
        self.page_line_text = QLineEdit()
        self.page_line_text.setPlaceholderText('输入整数')
        self.page_line_text.setValidator(QIntValidator(1, 99))
        self.page_line_text.setFocus()

        self.page_num_label = QLabel()
        self.page_num_label.setText('每页爬取数量：')
        self.page_num_text = QSpinBox()
        self.page_num_text.setRange(50, 100)
        self.page_num_text.setSingleStep(10)
        self.page_num_text.setWrapping(True)

        self.keyword_label = QLabel()
        self.keyword_label.setText('设置图关键字：')
        self.keyword_line_text = QLineEdit()
        self.keyword_line_text.setValidator(QRegExpValidator(QRegExp('[\u4E00-\u9FA5]+')))
        self.keyword_line_text.setMaxLength(6)
        self.keyword_line_text.setPlaceholderText('输入汉字')

        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText('自定义文件路径')
        self.file_path.setReadOnly(True)
        self.file_path_button = QPushButton()
        self.file_path_button.setText('自定义路径')
        self.file_path_button.clicked.connect(self.file_path_click)

        self.request_button = QPushButton()
        self.request_button.setText('快速开始抓取图片')
        self.request_button.clicked.connect(self.download_image)

        self.brower = QTextBrowser()
        self.brower.setPlaceholderText('抓取进度结果展示...')

        grid.addWidget(self.page_label, 0, 0, 1, 1)
        grid.addWidget(self.page_line_text, 0, 1, 1, 2)
        grid.addWidget(self.page_num_label, 1, 0, 1, 1)
        grid.addWidget(self.page_num_text, 1, 1, 1, 2)
        grid.addWidget(self.keyword_label, 2, 0, 1, 1)
        grid.addWidget(self.keyword_line_text, 2, 1, 1, 2)
        grid.addWidget(self.file_path, 3, 0, 1, 2)
        grid.addWidget(self.file_path_button, 3, 2, 1, 1)
        grid.addWidget(self.brower, 4, 0, 1, 3)
        grid.addWidget(self.request_button, 5, 0, 1, 3)

        self.thread_ = ScripyImages(self)
        self.thread_.trigger.connect(self.update_log)
        self.thread_.finished.connect(self.finished)

        self.setLayout(grid)

    def file_path_click(self):
        self.cwd = os.getcwd()
        directory = QFileDialog.getExistingDirectory(self, '选取文件夹', self.cwd)
        print(directory)
        self.file_path.setText(directory + '/')

    def update_log(self, text):
        '''
        槽函数：向文本浏览器中写入内容
        :param text:
        :return:
        '''
        cursor = self.brower.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.brower.append(text)
        self.brower.setTextCursor(cursor)
        self.brower.ensureCursorVisible()

    def finished(self, finished):
        if finished is True:
            self.request_button.setEnabled(True)

    def download_image(self):
        self.request_button.setEnabled(False)
        self.thread_.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    baidu = baiduImage()
    baidu.show()
    sys.exit(app.exec_())
