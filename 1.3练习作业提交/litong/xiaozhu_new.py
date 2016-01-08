from bs4 import BeautifulSoup
import requests
import time


url = 'http://bj.xiaozhu.com/search-duanzufang-p1-0/'

urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(1, 15)]


def get_houseInfo(url, data=None):

    time.sleep(2)
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    titles = soup.select('div.result_intro > a')
    imgs = soup.select('ul > li > a > img')
    addrs = soup.select('ul > li > div.result_btm_con.lodgeunitname > div > em')
    prices = soup.select('ul > li > div.result_btm_con.lodgeunitname > span.result_price > i')
    links = soup.select('ul > li > div.result_btm_con.lodgeunitname > span.result_img > a')

    if data == None:
        for title, img, addr, price, link in zip(titles, imgs, addrs, prices, links):
            homepage = link.get('href')
            ownerData = get_ownerInfo(homepage)

            a = addr.get_text()
            b = a.split()
            if len(b) == 5:
                data = {
                    'title': title.get_text(),
                    'img': img.get('src'),
                    'addr': b[4],
                    'price': price.get_text(),
                    'homepage': homepage,
            }
            if len(b) == 4:
                data = {
                    'title': title.get_text(),
                    'img': img.get('src'),
                    'addr': b[2],
                    'price': price.get_text(),
                    'homepage': homepage
            }

            print(ownerData)
            print(data)
            ownerData.update(data)
            print(ownerData)
            print ('\n --------------------------------------------- \n')


def get_ownerInfo(link, data=None):

    web_data = requests.get(link)
    soup = BeautifulSoup(web_data.text, 'lxml')
    gender = soup.select('div.person_infor > ul.fd_person > li')
    name = soup.select('div.person_infor > div.fd_name')
    photo = soup.select('div.person_infor > div.fd_img > img')
    if len(name) == 0:
        data = {
            'gender': 'Nan',
            'name': 'Nan',
            'photo': 'Nan'
        }
    else:
        data = {
            'gender': gender[0].get_text().replace('性别：', ''),
            'name': name[0].get_text().strip(),
            'photo': photo[0].get('src')
        }
    return data



for url in urls:
    get_houseInfo(url)
    break
    #get_ownerInfo(url)






