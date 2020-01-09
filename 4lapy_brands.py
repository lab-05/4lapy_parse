from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import os


file_addres = os.path.abspath('4lapybrands.csv')
# парсинг ссылок на бренды
html = urlopen('https://4lapy.ru/brand/')
bsObj = BeautifulSoup(html, "lxml")
bsObject = bsObj.find("div", {"class":"b-container b-container--brand-list"}).findAll("a", {"class":"b-popular-brand-item b-popular-brand-item--brands"})
#
list_url = []
list_name = []
for link in bsObject:
    list_url.append('https://4lapy.ru'+link.attrs['href'])
    list_name.append(link.attrs['title'])
    
    
result_frame = pd.DataFrame()
url_se = pd.Series(list_url)
name_se = pd.Series(list_name)
result_frame.insert(loc=0, column='Url', value=url_se)
result_frame.insert(loc=1, column='Name', value=list_name)
result_frame.to_csv(str(file_addres), sep=';', encoding="cp1251")