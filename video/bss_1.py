# coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
import sys
import os
from django.core.wsgi import get_wsgi_application
import django
sys.path.extend(['E:\\pythonproject\\django_env\\lyqVideo',])
os.environ.setdefault("DJANGO_SETTINGS_MODULE","lyqVideo.settings")
application = get_wsgi_application()
django.setup()
from video.models import *

def open_html(url):
    wdate = requests.get(url)
    wdate.encoding = 'gb2312'
    soup = BeautifulSoup(wdate.text, 'lxml')
    return soup


def select_html(html, select_path):
    new = html.select(select_path)
    return str(new)


# URL地址
url = 'https://www.dytt8.net/'
url_2 = 'https://www.dytt8.net/html/gndy/dyzz/20190412/58479.html'

# 定位元素路径
select_path = "#header > div > div.bd2 > div.bd3 > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(2) > div.co_content8 > ul > table > tr > td > a"

# 打开网页
html = open_html(url)

# 定位元素
result = select_html(html, select_path)

# 匹配信息
s = re.findall(r'/[a-z]+/[a-z]+/[a-z]+/[0-9]+/[0-9]+.html', result)

# 循环列出
for i in s:
    single_img = ''
    single_link = ''
    single_introduce = ''
    url_2 = url + i
    html = open_html(url_2)
    title = html.title.string
    s2 = html.find_all('img')
    s2 = str(s2)
    img = re.findall(r'https://[a-z]+.net/images/[0-9]+/[0-9]+/[0-9]+/[0-9a-z]+.jpg', s2)
    if img:
        single_img = img[0]


    ftp = re.findall('<a href="(.*?)">.*?</a></td>', str(html))
    if ftp:
        single_link = ftp[0]


    content = html.find_all('p')
    content2 = re.findall('<br/><br/>◎简　　介(.*?)<br/><br/>(.*?)<br/><br/>', str(html))
    for i in content2:
        i = list(i)
        single_introduce = i[1]


    v = Video.objects.get_or_create(
        name=title,
        img=single_img,
        link=single_link,
        introduce=single_introduce,
        cate=Cate.objects.get(name='迅雷电影资源'),
    )
    vv = Video.objects.get(
        name=title,
        img=single_img,
        link=single_link,
        introduce=single_introduce,
        cate=Cate.objects.get(name='迅雷电影资源'),
    )
    sets = Set.objects.create(
        name='迅雷电影资源',
        video=vv
    )

print("Done!")





