
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