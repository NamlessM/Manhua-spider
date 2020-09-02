import urllib.parse
import requests
from bs4 import BeautifulSoup

manhua_chapters = {}
url = 'www.manhuabei.com/manhua/nvpengyoujiewoyixia'
r = requests.get(url=url)
r.encoding = 'utf-8'
detail_info = BeautifulSoup(r.text, 'lxml')
detail_chapters_info = detail_info.find('ul', class_='list_con_li autoHeight')
detail_chapters_info = detail_chapters_info.find_all('a')

for chapter in detail_chapters_info:
    url = 'manhuabei.com' + chapter.get('href')
    chapter_name = chapter.get('title')
    manhua_chapters.update({chapter_name:url})
print(manhua_chapters)
'''
import requests
from bs4 import BeautifulSoup
target_url = "https://www.dmzj.com/info/yaoshenji.html"
r = requests.get(url=target_url)
bs = BeautifulSoup(r.text, 'lxml')
list_con_li = bs.find('ul', class_="list_con_li")
comic_list = list_con_li.find_all('a')
chapter_names = []
chapter_urls = []
for comic in comic_list:
    href = comic.get('href')
    name = comic.text
    chapter_names.insert(0, name)
    chapter_urls.insert(0, href)

print(chapter_names)
print(chapter_urls)'''
