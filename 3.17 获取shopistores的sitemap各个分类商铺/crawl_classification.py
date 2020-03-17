
import requests
from fake_useragent import UserAgent
import pandas as pd
from pyquery import PyQuery as pq
import time
import random
import os

class down_classification():
    def __init__(self,raw_url):
        self.filename=str(raw_url).replace('/','')
        self.url='https://www.shopistores.com'+raw_url


    def get_page(self,url):
        try:
            ua = UserAgent(verify_ssl=False)
            headers = {"User-Agent": ua.chrome}
            page = requests.get(url, headers=headers).text
            if 'ErrorException' in page:
                return 0
            return page
        except:
            return None
    def parse(self,page):
        page_data = pq(page)
        try:
            data = page_data('#content-container-tbl > table > tbody').text().split('\n')  # 通过css选择器定位
        except:
            pass
        else:
            shop_lst = []
            temp = []
            ##	 Num  Store Address	 Title	 Alexa	 Best Selling	Country
            for i in range(len(data)):
                if (i + 1) % 6 == 0:
                    temp.append(data[i])
                    shop_lst.append(temp)
                    temp = []
                else:
                    temp.append(data[i])
            self.save_to_csv(shop_lst)

    def save_to_csv(self,shop_list):
        data = pd.DataFrame(shop_list)
        data.to_csv(self.filename+'.csv', mode='a', index=False, sep=',', header=False, encoding='utf-8')
    def down(self):
        count = 1
        while True:
            url = self.url + str(count)
            try:
                page = self.get_page(url=url)
                if page == 0:
                    break
                else:
                   self.parse(page)
            except:
                count += 1
                continue
            else:
                #print('第' + str(count) + '页已下载！')
                count += 1


if __name__ == '__main__':
    lst = open('siemapresult.txt', 'r', encoding='utf-8').read().split('\n')
    os.chdir(r'D:\a\tempdata\3.17')
    for i in range(len(lst)):
        spi = down_classification(lst[i])
        spi.down()






