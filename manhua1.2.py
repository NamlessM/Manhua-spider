import requests
import urllib.parse
from bs4 import BeautifulSoup
import time
from multiprocessing.dummy import Pool as ThreadPool
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image,ImageEnhance
from urllib.request import urlretrieve
import re

usersearch_dic = {}
userchoose_dic = {}
manhua_chapters = {}
manhua_chapters_titles = {}
pic_link_dic = {}

# 创建浏览器对象
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=chrome_options)



def welcome():
    print('欢迎回来，今天你干正经事了吗？手动狗头')
    time.sleep(1)
    print('坚持要看漫画那我还能说啥呢')
    time.sleep(1)

def get_book():
    global user_book
    user_book = input('请输入想康的漫画：')
    url_user_book = urllib.parse.quote(user_book)
    search_url = "https://www.manhuabei.com/search/?keywords=" + url_user_book
    search_header = {
        'Referer':'https://www.manhuabei.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    search_params = {
        'keywords' : user_book
    }
    
    r = requests.get(url = search_url, params = search_params, headers = search_header)
    r.encoding = 'utf-8'
    search_html_all = BeautifulSoup(r.text, 'lxml')
    search_html = search_html_all.find_all('a', class_ = 'image-link')
    count = 1
    for ani in search_html:
        url = ani.get('href')
        title = ani.get('title')
        usersearch_dic.update({str(count)+title:url})
        userchoose_dic.update({str(count):url})
        count += 1
        ''' 搜索并储存名字和url为2个字典'''

def choose():
    print('我们为您检索到了：')
    print(list(usersearch_dic.keys()))
    global user_num
    global choosen_url
    user_num = input('请您输入序号:')
    choosen_url = userchoose_dic[user_num]

def get_detail_info():
    r = requests.get(url=choosen_url)
    r.encoding = 'utf-8'
    global detail_info
    detail_info = BeautifulSoup(r.text, 'lxml')
    detail_intro = detail_info.find('p', class_ = 'comic_deCon_d')
    print('以下是简介')
    time.sleep(1)
    print(detail_intro.get_text("|",strip = True))

def confirmation():
    global user_response 
    user_response = input("搜到的OK不，yes or no：")

    while user_response == 'no':
        print('请重新选择')
        choose()
        get_detail_info()
        confirmation()
    
    if user_response == 'yes':
        pass
    else:
        print('yes or no!!!!')
        confirmation()

def chapters():
    detail_chapters_info = detail_info.find('ul', class_='list_con_li autoHeight')
    detail_chapters_info = detail_chapters_info.find_all('a')

    count = 1
    print('以下是检索到的章节目录')
    time.sleep(1)
    for chapter in detail_chapters_info:
        url = 'manhuabei.com' + chapter.get('href')
        chapter_name = chapter.get('title')
        manhua_chapters.update({count:url})
        manhua_chapters_titles.update({count : chapter_name})
        count += 1
    print(manhua_chapters_titles)

def choose_chapters():
    chapter_initial = input('请您输入下载起始章节序号（e.g.下载5到8请输入5）')
    chapter_end = input('请输入下载结束章节序号（e.g下载5到8请输入8）')
    for i in range(int(chapter_end)+1,len(manhua_chapters_titles)+1):
        del manhua_chapters[i]
        del manhua_chapters_titles[i]
    for i in range(1, int(chapter_initial)):
        del manhua_chapters[i]
        del manhua_chapters_titles[i]
    global inverse_search
    inverse_search = {v: k for k, v in manhua_chapters_titles.items()}
    print(manhua_chapters_titles)           

def get_image_link(url,a):
#打开浏览器
    driver.get(url=url +'?p='+str(a))
    soup = BeautifulSoup(driver.page_source,'html.parser')
    tag = soup.find('div', id = 'images')
    tag_string = str(tag)
    list_tag = tag_string.split()
    urls = list_tag[3]
    urlss = urls[5:-1]
    return urlss

def collect_link(url):
    driver.get(url+'?p=1')
    soup = BeautifulSoup(driver.page_source,'html.parser')
    tag = soup.find('div', id = 'images')
    tags = str(tag.find('p', class_ = 'img_info'))
    return(int(tags[23:25]))


def downvideo_for_one_chapter(i):
    t = get_image_link('https://'+url,i)
    print(t)
    print(i)
    detail_path = path + '/' +str(i)+'.jpg'
    urlretrieve(t,detail_path)
            
'''
TODO:
增加误差处理，跳过无法下载章节
检测文件夹是否存在
处理链接超时问题
'''

if __name__ == "__main__":
    welcome()
    get_book()
    choose()
    get_detail_info()
    confirmation()
    chapters()
    choose_chapters()
    intended_chpaters = list(manhua_chapters_titles.values())
    for chaptertitle in intended_chpaters:
        path = str(user_book)+'/'+str(chaptertitle)
        num = inverse_search[chaptertitle]
        url = manhua_chapters[num]
        if path not in  os.listdir('./'):
            if user_book not in os.listdir('./'):
                os.mkdir(user_book)
            os.mkdir(path)
            x = collect_link('https://'+url)
            y = list(range(1,x+1))
            pool = ThreadPool(3)
            results = pool.map(downvideo_for_one_chapter,y)
            pool.close()
            pool.join()


