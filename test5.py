from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image,ImageEnhance
 
 
#path = 'C:\Users\MikeY\AppData\local\Programs\Python\Python38-32\chromedriver.exe'
 
#打开浏览器
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 创建浏览器对象
driver = webdriver.Chrome(options=chrome_options)
for a in range(1,10):
    driver.get(url='https://www.manhuabei.com/manhua/jinjidejuren/170376.html?p='+str(a))
    soup = BeautifulSoup(driver.page_source,'html.parser')
    tag = soup.find('div', id = 'images')
    tag_string = str(tag)
    list_tag = tag_string.split()
#print(list_tag)
    urls = list_tag[3]
    urlss = urls[5:-1]
    print(urlss)





