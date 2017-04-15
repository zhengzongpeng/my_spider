
import xlwt
import xlrd
from bs4 import BeautifulSoup
from urllib import request
from urllib import error
from xlutils.copy import copy
import time

excel_file_name = "my_text2.xls"
#url = 'http://bj.lianjia.com/chengjiao/101100989652.html'
origin_url = 'http://sz.lianjia.com/ershoufang/'
def get_house_urls(url):
    url = origin_url + url
    req = request.urlopen(url)
    src_code = req.read()
    soup = BeautifulSoup(src_code, 'lxml')
    tags = soup.find_all('div', {'class':'item'})
    url_list = []

    for tag in tags:
        #print(tag)
        try:
            url_list.append(tag.a['href'])
        except AttributeError as e:
            continue
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
    community_info = soup.find('div', {'class':'communityName'})
    ## 小区名
    try:
        house_info.append(community_info.a.get_text())
    except AttributeError as e:
        print (e)
    # get price info
    #tag_price = soup.find('div', {'class':'price'})
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
    write_count = 0
    for page in range(1, 10):
        str_url = ""
        if page > 1:
            str_url = "pg" + str(page)
        time.sleep(8)
        house_urls = get_house_urls(str_url)
        print ("ready to get " + str(len(house_urls)) + " houses info from " + str_url)
        rb = xlrd.open_workbook(excel_file_name)
        wb = copy(rb)
        ws = wb.add_sheet("page" + str(page))
        for i, url in enumerate(house_urls):
            print("getting info from  " + url + " ....")
            time.sleep(8)
            data_ary = get_house_info(url)
            if isinstance(data_ary, int):
                print ("failed to fetch url " + url)
                continue
            data_ary.append(url)
            print(write_count, "total " + str(len(house_urls)) + " writing data " + data_ary[0] + " to excel......")
            for j in range(0, len(data_ary)):
                ws.write(write_count, j, data_ary[j])
            write_count = write_count + 1
        wb.save("my_text2.xls")

    print ("save the excel file")



