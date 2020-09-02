from selenium import webdriver


browser = webdriver.Chrome()
browser.get('http://www.manhuabei.com/manhua/jinjidejuren/170376.html?p=2/')
print(browser.page_source)