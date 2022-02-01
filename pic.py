from bs4 import BeautifulSoup
import requests
import os
import re

urlHead = 'https://photo.fengniao.com/'
url = 'https://photo.fengniao.com/pic_43591143.html'


def getHtmlurl(url):  # 获取网址
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def getpic(html):  # 获取图片地址并下载，再返回下一张图片地址
    soup = BeautifulSoup(html, 'html.parser')
    # all_img = soup.find('div', class_='imgBig').find_all('img')

    all_img = soup.find('a', class_='downPic')
    img_url = all_img['href']

    reg = r'<h3 class="title overOneTxt">(.*?)</h3>'  # r'<a\sclass=".*?"\starget=".*?"\shref=".*?">(.*)</a>'  # 正则表达式
    reg_ques = re.compile(reg)  # 编译一下正则表达式，运行的更快
    image_name = reg_ques.findall(html)  # 匹配正则表达式

    urlNextHtml = soup.find('a', class_='right btn')
    urlNext = urlHead + urlNextHtml['href']

    print('正在下载：' + img_url)
    root = 'D:/pic/'
    path = root + image_name[0] + '.jpg'
    try:  # 创建或判断路径图片是否存在并下载
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(img_url)
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print("图片下载成功")
        else:
            print("文件已存在")
    except:
        print("爬取失败")
    return urlNext


def main():
    html = (getHtmlurl(url))
    print(html)
    return getpic(html)


if __name__ == '__main__':
    for i in range(1, 100):
        url = main()