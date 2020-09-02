import os
import ffmpy3
import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import time
search_dic = {}
user_dic_url = {}
user_dic_name = {}
serach_res = {}
def search():
    search_keyword = input('请您输入想康的番：')
    search_url = 'http://www.jisudhw.com/index.php'
    serach_params = {
        'm': 'vod-search'
    }
    serach_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
        'Referer': 'http://www.jisudhw.com/',
        'Origin': 'http://www.jisudhw.com',
        'Host': 'www.jisudhw.com'
    }
    serach_datas = {
        'wd': search_keyword,
        'submit': 'search'
    }



    r = requests.post(url=search_url, params=serach_params,
                    headers=serach_headers, data=serach_datas)
    r.encoding = 'utf-8'
    server = 'http://www.jisudhw.com'
    search_html = BeautifulSoup(r.text, 'lxml')
    search_spans = search_html.find_all('span', class_='xing_vb4')

    count = 1
    for span in search_spans:
        url = server + span.a.get('href')
        name = span.a.string
        search_dic.update({str(count) + name: url})
        user_dic_name.update({str(count): name})
        user_dic_url.update({str(count): url})
        count += 1



def choose():
    global detail_url
    print('我们为您检索到了：')
    time.sleep(0.5)
    print(list(search_dic.keys()))
    time.sleep(0.5)
    global user_num
    user_num = input('请您输入想要的剧集(输入序号即可）：')
    detail_url = user_dic_url[user_num]    
    
def getvideodetail():
    r = requests.get(url=detail_url)
    r.encoding = 'utf-8'
    global detail_bf
    detail_bf = BeautifulSoup(r.text, 'lxml')
    detail_intro = detail_bf.find('div', class_ ='vodplayinfo')
    print('这是它的简介')
    print(detail_intro.text.strip())

def confirmation():
    global a
    print('请问这是否是您想康的影片：')
    a = input('如果是的话请您输入yes,不是请输入no：')

def down():   
    num = 1
    for each_url in detail_bf.find_all('input'):
        if 'm3u8' in each_url.get('value'):
            # print(each_url.get('value'))
            url = each_url.get('value')
            if url not in serach_res.values():
                serach_res[num] = url
            #print('第%03d集:' % num)
            # print(url)
            num += 1
    time.sleep(1)
    print('为您检测到了站点含有如下集数')
    print(list(serach_res.keys()))
    search_num_initial = input('请您输入想下载的起始剧集（如您想下载第五集到第九集请输入5）:')
    search_num_final = input('请您输入想下载的结束剧集（如您想下载第五集到第九集请输入9）:')
    for i in range(int(search_num_final)+1, len(serach_res)+1):
        del serach_res[i]
    for i in range(1, int(search_num_initial)):
        del serach_res[i]
    global inverse_search
    inverse_search  = {v: k for k, v in serach_res.items()}

def makedir():
    global video_dir
    video_dir = user_dic_name[user_num]
    if video_dir not in os.listdir('./'):
        os.mkdir(video_dir)
def downVideo(url):
    #num = serach_res[url]
    num = inverse_search[url]
    # 解决通过值找键
    name = os.path.join(video_dir, '第%03d集.mp4' % num)
    ffmpy3.FFmpeg(inputs={url: None}, outputs={name: None}).run()
# 开8个线程池




#输入想要搜索的
#输入是否是想要的：Y - 爬取所有剧集 N-返回上一级爬取的列表

search()
choose()
getvideodetail()
confirmation()
while a == 'no':
    choose()
    getvideodetail()
    confirmation()
down()
makedir()
pool = ThreadPool(int(input('今日想开几线程呢：')))
results = pool.map(downVideo, serach_res.values())
pool.close()
pool.join()
