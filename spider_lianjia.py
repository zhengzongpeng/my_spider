
from urllib import error
from urllib import request

from bs4 import BeautifulSoup

url = 'http://sz.lianjia.com/chengjiao/'

def get_all_houses_links(state, page_num = 0):
    url2 = url + state
    print(url2)
    src_code = request.urlopen(url2).read()
    soup = BeautifulSoup(src_code, 'lxml')
    urls = []
    for tag in soup.find_all('a', {'class':'img'}):
        urls.append(tag.get('href'))
    for tmp in urls:
        print (tmp)


if __name__ == '__main__':
    get_all_houses_links('nanshanqu')
	
	
	
from bs4 import BeautifulSoup
from urllib import request
import re

#url = 'http://bj.lianjia.com/chengjiao/101100989652.html'
url = 'http://sz.lianjia.com/ershoufang/'
def get_house_urls():
    req = request.urlopen(url)
    src_code = req.read()

    soup = BeautifulSoup(src_code, 'lxml')

    tags = soup.find_all('div', {'class':'item'})
    url_list = []
    for tag in tags:
        #print(tag)
        url_list.append(tag.a['href'])
        return url_list
#print(soup.find('div', {'data-houseid':'101101106545'}))
#print(soup.find('a', {'href':'http://bj.lianjia.com/zufang/'}))

def get_house_info(url):
    req = request.urlopen(url)
    src_code = req.read()
    soup = BeautifulSoup(src_code, 'lxml')
    # get price info
    tag_price = soup.find('div', {'class':'price'})
    print(tag_price)
    for tmp in soup.find_all("span"):
        if "class" in tmp.attrs:
            if "total" in tmp.attrs["class"]:
                total_price = tmp.get_text()
                print ('total price :' + total_price + '万')
            if "unitPriceValue" in tmp.attrs["class"]:
                unit_price = tmp.get_text()
                print('unit price :' + unit_price)
            if "label" in tmp.attrs["class"]:
                if str(tmp.get_text()) == "挂牌时间":
                    print(tmp.find_parent("li").get_text(": "))
                elif str(tmp.get_text()) == "上次交易":
                    print(tmp.find_parent("li").get_text(": "))
    for tmp in soup.find_all("li", text = "<span>"):
        print (tmp)
    # get house info
    tag_house_info = soup.find('div', {'class':'houseInfo'})
    unit_type = tag_house_info.find('div', {'class':'room'}).find('div', {'class':'mainInfo'}).get_text()
    total_area = tag_house_info.find('div', {'class': 'area'}).find('div', {'class': 'mainInfo'}).get_text()
    #print (tag.find('span', {'class':'total'}))

def write_to_excel(data):
    return

if __name__ == '__main__':
    house_urls = get_house_urls()
    data = get_house_info(house_urls[0])
    write_to_excel(data)
    #for house_url in house_urls:


#    for url in  house_urls:
#        get_house_info(url)

