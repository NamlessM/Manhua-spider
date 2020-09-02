import os
import requests
from urllib.request import urlretrieve
x = 'sds'
path = x + '/'+'1.jpg'
os.mkdir(x)
dn_url = 'https://img01.eshanyao.com/images/comic/86/170376/1555606943ykOso5IP866A-pgu.jpg'
urlretrieve(dn_url,path)