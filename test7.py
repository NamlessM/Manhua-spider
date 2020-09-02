pic_link_dic = {}
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image,ImageEnhance
import urllib
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

    # 创建浏览器对象
driver = webdriver.Chrome(options=chrome_options)
'''def get_image_link(a):
 
 
#打开浏览器

    driver.get(url='https://www.manhuabei.com/manhua/jinjidejuren/170376.html?p='+str(a))
    soup = BeautifulSoup(driver.page_source,'html.parser')
    tag = soup.find('div', id = 'images')
    tag_string = str(tag)
    #print(tag)
    list_tag = tag_string.split()
    #print(list_tag)
    urls = list_tag[3]
    urlss = urls[5:-1]
    #print(urls)
    pic_link_dic.update({a:urlss})'''

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

get_image_link('manhuabei.com/manhua/nvpengyoujiewoyixia/174373.html',2)
'''for i in range(1,collect_link('https://www.manhuabei.com/manhua/jinjidejuren/170376.html')+1):
    get_image_link(i)
    os.mkdir('巨人')
    detail_path = path + '/' +str(i)+'.jpg'
    urlretrieve(pic_link_dic[i],detail_path)'''






    
    