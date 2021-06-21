nomerbrenda = 156

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd

# парсинг ссылок на бренды
html = urlopen('https://4lapy.ru/brand/')
bsObj = BeautifulSoup(html, "lxml")
bsObject = bsObj.find("div", {"class":"b-container b-container--brand-list"}).findAll("a", {"class":"b-popular-brand-item b-popular-brand-item--brands"})
list_url = []
for link in bsObject:
    list_url.append('https://4lapy.ru'+link.attrs['href'])


product_weight_text = []
product_name_text = []
product_price_text = []


#Последний вариант - вроде бы работает
#проходим по каждой из страниц пагинации и добавляем название, цену и вес товаров в общий список - почти рабочая версия, не проверяет только разные веса и фасовки
for j in list_url[nomerbrenda:nomerbrenda+1]: # перебираем значения из list_url - списка брендова
    pagination_list = []
    bsObj_pl = BeautifulSoup(urlopen(str(j)), "lxml")
    search = bsObj_pl.find("div", {"class":"b-pagination"}) #проверяем наличие на странице блока пагинации
    if (search is not None):    #если блок есть, то начинаем обработку
        pagination_last = bsObj_pl.find("div", {"class":"b-pagination"}).find("li", {"class":"b-pagination__item b-pagination__item--next"}).previousSibling.previousSibling.a.attrs['title'] #находим в блоке пагинации элемент "вперед" и считываем значение предыдущего элемента(который и есть количество страниц пагинации)
        pagination_list = [ii for ii in range(1,int(pagination_last)+1)] # по значению из предыдущего шага делаем список соответствующей длины
        for i in pagination_list:
            bsObj = BeautifulSoup(urlopen(str(j)+'?brand_code=&page='+str(i)), "lxml") # делаем обход по страницам пагинации
            #bsObj = BeautifulSoup(urlopen(str(j)+'?page='+str(i)), "lxml") # делаем обход по страницам пагинации
            quality_product_on_page = len(bsObj.find("div", {"class":"b-common-wrapper b-common-wrapper--visible js-catalog-wrapper"}).findAll("div", {"class":"b-common-item__info-center-block"}))
            for prods in range(quality_product_on_page):
                weight_list = bsObj.find("div", {"class":"b-common-wrapper b-common-wrapper--visible js-catalog-wrapper"}).findAll("div", {"class":"b-common-item__info-center-block"})[prods].findAll("li", {"class":"b-weight-container__item"}) #находим элемент в котором хранятся все фасовки этого товара
                #if len(weight_list)>1:  
                for wl in weight_list:
                    product_name_text.append(wl.parent.parent.parent.find("span", {"class": "b-clipped-text b-clipped-text--three"}).text)
                    product_price_text.append(wl.a.attrs["data-price"])
                    product_weight_text.append(wl.get_text())
    if (search is None):
        quality_product_on_page1 = len(bsObj_pl.find("div", {"class":"b-common-wrapper b-common-wrapper--visible js-catalog-wrapper"}).findAll("div", {"class":"b-common-item__info-center-block"}))
        for prods in range(quality_product_on_page1):
            weight_list1 = bsObj_pl.find("div", {"class":"b-common-wrapper b-common-wrapper--visible js-catalog-wrapper"}).findAll("div", {"class":"b-common-item__info-center-block"})[prods].findAll("li", {"class":"b-weight-container__item"}) #находим элемент в котором хранятся все фасовки этого товара
            for wl1 in weight_list1:
                product_name_text.append(wl1.parent.parent.parent.find("span", {"class": "b-clipped-text b-clipped-text--three"}).text)
                product_price_text.append(wl1.a.attrs["data-price"])
                product_weight_text.append(wl1.get_text())        

        
product_name_text = [re.sub('\n|\s{16,19}','',els) for els in product_name_text]
product_weight_text = [re.sub('\n|\s{16,19}','',irr) for irr in product_weight_text]


result_frame = pd.DataFrame()
name_se = pd.Series(product_name_text)
weight_se = pd.Series(product_weight_text)
price_se = pd.Series(product_price_text)
result_frame.insert(loc=0, column='Name', value=name_se)
result_frame.insert(loc=1, column='Weight', value=weight_se)
result_frame.insert(loc=2, column='Price', value=price_se)
result_frame.to_csv('Путь на локальном компьютере для сохранения файла', sep=';', encoding="cp1251")
#path_to_file = os.path.abspath('4lapy.csv')
#result_frame.to_csv(path_to_file, sep=';', encoding="cp1251")
