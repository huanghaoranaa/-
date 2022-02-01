# -*- coding:utf-8 -*-

# requests网络请求库

import requests

# UserAgent生成库

from fake_useragent import UserAgent

from PyQt5.QtCore import *


class ScripyImages(QThread):

    trigger = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, parent):
        super(ScripyImages, self).__init__(parent)
        self.parent = parent
        self.user_agent = UserAgent()
        self.working = True

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        page = self.parent.page_line_text.text().strip()
        key_word = self.parent.keyword_line_text.text().strip()
        save_dir = self.parent.file_path.text().strip()
        num_one_page = self.parent.page_num_text.value()
        self.trigger.emit("设置数据读取完成！")

        self.request_init(page, key_word, save_dir, num_one_page)

    def request_init(self, page, key_word, save_dir, num_one_page):
        # 设置请求头
        self.headers = {
            'User-Agent': self.user_agent.random
        }
        self.trigger.emit("HTTP请求头设置完成！")
        # 设置从某一页的第几张图片开始爬取
        current_page_nums = 0
        pic_ser = 0
        for m in range(1, int(page) + 1):
            self.trigger.emit("开始第[" + str(m) + "]页图片读取！")
            url = 'https://image.baidu.com/search/acjson?'
            params = {
                'tn': 'resultjson_com',
                'logid': '',
                'ipn': 'rj',
                'ct': '201326592',
                'is': '',
                'fp': 'result',
                'queryWord': str(key_word),
                'cl': '2',
                'lm': '-1',
                'ie': 'utf-8',
                'oe': 'utf-8',
                'adpicid': '',
                'st': '-1',
                'z': '',
                'ic': '',
                'hd': '',
                'latest': '',
                'copyright': '',
                'word': str(key_word),
                's': '',
                'se': '',
                'tab': '',
                'width': '',
                'height': '',
                'face': '0',
                'istype': '2',
                'qc': '',
                'nc': '1',
                'fr': '',
                'expermode': '',
                'force': '',
                'cg': '',
                'pn': current_page_nums,
                'rn': str(num_one_page),
                'gsm': '1e',
            }
            # 执行请求
            self.response = requests.get(url=url, headers=self.headers, params=params)
            self.trigger.emit("完成第[" + str(m) + "]页图片读取！")
            self.trigger.emit("开始下载第[" + str(m) + "]页图片！")
            # 定义结果编码
            self.response.encoding = 'utf-8'
            # 获取响应的json数据
            self.response = self.response.json()
            # 获取data键数据列表
            result_list = self.response['data']
            del result_list[-1]
            # 定义图片路径列表
            self.img_paths = []
            # 遍历获取图片路径到img_paths
            for i in result_list:
                # 提取图片地址
                self.img_paths.append(i['thumbURL'])
            for img_path in self.img_paths:
                # 执行图片下载
                img = requests.get(url=img_path, headers=self.headers).content
                # 设置图片保存路径
                img_path = str(save_dir) + str(pic_ser) + '.jpg'
                with open(img_path, 'wb') as fp:
                    # 保存图片
                    fp.write(img)
                    pic_ser = pic_ser + 1
                self.trigger.emit(img_path + '保存成功！')
            current_page_nums = current_page_nums + (int(num_one_page) - 1)
            self.trigger.emit("完成下载第[" + str(m) + "]页图片！")
        self.finished.emit(True)
