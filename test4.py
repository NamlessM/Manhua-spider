
from bs4 import BeautifulSoup 
from selenium import webdriver
 
urls = ('http://gkcx.eol.cn/soudaxue/queryProvince.html?page={}'.format(i) for i in range(1,166))
 
driver=webdriver.Chrome()
 
driver.maximize_window()
 
for url in urls:
    #print ("正在访问{}".format(url))
    driver.get(url)
    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')
    grades = soup.find_all('tr')
    for grade in grades:
        if '<td>' in str(grade):
            print(grade.get_text())
