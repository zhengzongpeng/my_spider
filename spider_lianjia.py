
import xlwt
import xlrd
from bs4 import BeautifulSoup
from urllib import request
from urllib import error
import re

#url = 'http://bj.lianjia.com/chengjiao/101100989652.html'
origin_url = 'http://sz.lianjia.com/ershoufang/'
def get_house_urls(url):
    url = origin_url + url
    print (url)
    req = request.urlopen(url)
    src_code = req.read()
    soup = BeautifulSoup(src_code, 'lxml')
    print(soup)
    tags = soup.find_all('div', {'class':'item'})
    url_list = []

    for tag in tags:
        #print(tag)
        url_list.append(tag.a['href'])
    print (" get_house_urls size " + str(len(url_list)))
    return url_list

#print(soup.find('div', {'data-houseid':'101101106545'}))
#print(soup.find('a', {'href':'http://bj.lianjia.com/zufang/'}))

def get_house_info(url):
    try:
        req = request.urlopen(url)
    except error.HTTPError as e:
        print (e.code)
        return e.code
    else:
        src_code = req.read()
    soup = BeautifulSoup(src_code, 'lxml')
    house_info = []
    # get price info
    tag_price = soup.find('div', {'class':'price'})
    #print(tag_price)
    for tmp in soup.find_all("span"):
        if "class" in tmp.attrs:
            if "total" in tmp.attrs["class"]:
                # 总价
                total_price = tmp.get_text()
                #print ('total price :' + total_price + '万')
                house_info.append(total_price)
            if "unitPriceValue" in tmp.attrs["class"]:
                # 单价
                unit_price = tmp.get_text()
                #print('unit price :' + unit_price)
                house_info.append(unit_price)
            if "label" in tmp.attrs["class"]:
                if str(tmp.get_text()) == "挂牌时间":
                    str_tmp = tmp.find_parent("li").get_text(":")
                    house_info.append(str_tmp.split(':')[1])
                elif str(tmp.get_text()) == "上次交易":
                    str_tmp = tmp.find_parent("li").get_text(":")
                    house_info.append(str_tmp.split(':')[1])

    # get house info
    tag_house_info = soup.find('div', {'class':'houseInfo'})
    #print (tag_house_info)
    unit_type = tag_house_info.find('div', {'class':'room'}).find('div', {'class':'mainInfo'}).get_text()
    house_info.append(unit_type)
    total_area = tag_house_info.find('div', {'class': 'area'}).find('div', {'class': 'mainInfo'}).get_text()
    house_info.append(total_area)
    #print (tag.find('span', {'class':'total'}))
    return house_info

def write_to_excel(data):
    return

if __name__ == '__main__':
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Test Sheet")
    write_count = 0
    for page in range(1, 20):
        str_url = ""
        if page > 1:
            str_url = "pg" + str(page)
        house_urls = get_house_urls(str_url)
        print ("ready to get " + str(len(house_urls)) + " houses info from " + str_url)
        for i, url in enumerate(house_urls):
            print("getting info from  " + url + " ....")
            data_ary = get_house_info(url)
            if isinstance(data_ary, int):
                print ("failed to fetch url " + url)
                continue
            data_ary.append(url)
            print(write_count, "total " + str(len(house_urls)) + " writing data " + data_ary[0] + " to excel......")
            for j in range(0, len(data_ary)):
                ws.write(write_count, j, data_ary[j])
            write_count = write_count + 1
    print ("save the excel file")
    wb.save("my_text2.xls")

    #for house_url in house_urls:


#    for url in  house_urls:
#        get_house_info(url)

